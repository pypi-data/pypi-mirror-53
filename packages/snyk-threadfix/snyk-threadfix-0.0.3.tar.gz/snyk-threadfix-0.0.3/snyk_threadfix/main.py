import sys
import argparse
import json
import snyk
import hashlib
import arrow
from sys import stderr
from snyk_threadfix.utils import get_token, validate_token


snyk_token = None
client = None
debug = False


class SnykTokenError(Exception):
    pass


class SnykTokenNotFoundError(SnykTokenError):
    pass


class SnykTokenInvalidError(SnykTokenError):
    pass


def log(msg):
    global debug
    if debug:
        print(msg, file=stderr)


def parse_command_line_args(command_line_args):
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--projectIds", type=str, help="Comma-separated list of Snyk project IDs", required=True
    )
    parser.add_argument('--output', type=str,
                        help='Optional: name output file to write to (should use .threadfix extension).',
                        required=False)
    parser.add_argument(
        "--debug", action='store_true', help="Send additional debug info to stderr", required=False)

    args = parser.parse_args(command_line_args)

    str_project_ids = args.projectIds

    if not str_project_ids:
        sys.exit('--projectIds input parameter is required')

    project_ids = str_project_ids.split(',')
    if len(project_ids) > 0:
        args.project_ids = project_ids
    else:
        sys.exit('--projectIds input parameter is required')

    return args


def parse_snyk_project_name(project_name):
    project_repo_name_and_branch = project_name.split(':')[0]
    project_target_file = project_name.split(':')[1]
    project_repo_name = project_repo_name_and_branch.split('(')[0]

    project_branch_name = None
    if '(' in project_repo_name_and_branch:
        # after the '(' and before the ')'
        project_branch_name = project_repo_name_and_branch.split('(')[1].split(')')[0]

    project_meta_data = {
        'repo': project_repo_name,
        'targetFile': project_target_file
    }

    if project_branch_name:
        project_meta_data['branch'] = project_branch_name

    return project_meta_data


def lookup_project_ids_by_repo_name_py_snyk(org_id, repo_name, origin, branch, target_file):
    """not used, but keeping it around for possible future use"""
    git_repo_project_origins = [
        'github',
        'github-enterprise',
        'gitlab',
        'bitbucket-cloud',
        'bitbucket-server',
        'azure-repos'
    ]

    projects = client.organizations.get(org_id).projects.all()

    matching_project_ids = []

    for p in projects:
        if p.origin in git_repo_project_origins:
            project_name_details = parse_snyk_project_name(p.name)

            if repo_name == project_name_details['repo'] and \
                    (not branch or branch and branch == project_name_details['branch']) and \
                    (not origin or origin and origin == p.origin) and \
                    (not target_file or target_file and target_file == project_name_details['targetFile']):
                log('Found project with matching repo name:')
                log('  %s' % p.name)
                log('  %s' % p.id)
                log('  %s\n' % p.origin)
                matching_project_ids.append(p.id)

    return matching_project_ids


def generate_native_id(org_id, project_id, issue_id, path_list):
    path_str = '>'.join(path_list)
    unhashed = '%s:%s:%s:%s' % (org_id, project_id, issue_id, path_str)

    sha1_hash = hashlib.sha1()
    b = bytes(unhashed, 'utf-8')
    sha1_hash.update(b)
    hashed_native_id = sha1_hash.hexdigest()

    return hashed_native_id


def snyk_identifiers_to_threadfix_mappings(snyk_identifiers_list):
    mappings = []

    identifier_keys = snyk_identifiers_list.keys()
    primary_key = ''
    primary_set = False

    if 'CWE' in identifier_keys and snyk_identifiers_list['CWE']:
        primary_key = 'CWE'
    elif 'ALTERNATIVE' in identifier_keys and snyk_identifiers_list['ALTERNATIVE']:
        primary_key = 'ALTERNATIVE'
    elif 'CVE' in identifier_keys and snyk_identifiers_list['CVE']:
        primary_key = 'CVE'
    elif 'NSP' in identifier_keys and snyk_identifiers_list['NSP']:
        primary_key = 'NSP'

    for k, v_list in snyk_identifiers_list.items():
        if v_list:
            for v in v_list:
                is_primary = False
                if k == primary_key and not primary_set:
                    is_primary = True
                    primary_set = True

                mapping_value = v.replace("CWE-", "") if k == 'CWE' else v

                mappings.append({
                    "mappingType": k,
                    "value": mapping_value,
                    "primary": is_primary
                })

    return mappings


def create_threadfix_findings_data(org_id, project_id):
    p = client.organizations.get(org_id).projects.get(project_id)
    findings = []
    project_meta_data = parse_snyk_project_name(p.name)
    target_file = project_meta_data['targetFile']

    for i in p.vulnerabilities:
        native_id = generate_native_id(org_id, project_id, i.id, i.fromPackages)

        finding = {
            'nativeId': native_id,
            'severity': i.severity,
            'nativeSeverity': i.cvssScore,
            'summary': i.title,
            'description': 'You can find the description here: %s' % i.url,
            'scannerDetail': 'You can find the description here: %s' % i.url,
            'scannerRecommendation': i.url,  # TBD
            'dependencyDetails': {
                'library': i.package,
                'description': 'You can find the description here: %s' % i.url,
                'reference': i.id,
                'referenceLink': "%s#issue-%s" % (p.browseUrl, i.id),
                'filePath': target_file,
                'version': i.version,
                'issueType': 'VULNERABILITY',
            },
            'metadata': {
                "language": i.language,  # TODO: figure out what this means for CLI/container project types
                "packageManager": i.packageManager,  # TODO: figure out what this means for CLI/container project types
                "CVSSv3": i.CVSSv3,
                "cvssScore": i.cvssScore,
                "snyk_source": p.origin,
                "snyk_project_id": project_id,
                "snyk_project_name": p.name,
                "snyk_repo": project_meta_data['repo'],
                "snyk_branch": project_meta_data.get('branch', '(default branch)'),
                "snyk_target_file": project_meta_data['targetFile'],
                "snyk_project_url": p.browseUrl,
                "snyk_organization": org_id
            },

            'mappings': []
        }

        mappings = snyk_identifiers_to_threadfix_mappings(i.identifiers)
        finding['mappings'] = mappings
        findings.append(finding)

    return findings


def write_to_threadfix_file(output_filename, threadfix_json_obj):
    log('Writing output threadfix file: %s' % output_filename)

    with open(output_filename, 'w') as output_json_file:
        json.dump(threadfix_json_obj, output_json_file, indent=4)


def write_output_to_stdout(threadfix_json_obj):
    json.dump(threadfix_json_obj, sys.stdout, indent=4)


def main(args):
    global snyk_token, client, debug
    args = parse_command_line_args(args)
    debug = args.debug

    snyk_token = get_token()
    token_is_valid = validate_token(snyk_token)
    if not token_is_valid:
        raise SnykTokenInvalidError('invalid token')

    client = snyk.SnykClient(snyk_token)

    # project_ids = lookup_project_ids_by_repo_name_py_snyk(args.orgId, repo_name, origin, branch, target_file)
    project_ids = args.project_ids

    current_time = arrow.utcnow().replace(microsecond=0)
    current_time_str = current_time.isoformat().replace("+00:00", "Z")

    threadfix_json_obj = {
        'created': current_time_str,  # All timestamps are to be in yyyy-MM-dd'T'HH:mm:ss'Z' format
        'exported': current_time_str,  # All timestamps are to be in yyyy-MM-dd'T'HH:mm:ss'Z' format
        'collectionType': 'DEPENDENCY',
        'source': 'Snyk',
        'findings': []
    }

    all_threadfix_findings = []

    for p_id in project_ids:
        threadfix_findings = create_threadfix_findings_data(args.orgId, p_id)
        all_threadfix_findings.extend(threadfix_findings)

    threadfix_json_obj['findings'] = all_threadfix_findings
    write_output_to_stdout(threadfix_json_obj)
    if args.output:
        write_to_threadfix_file(args.output, threadfix_json_obj)


def run():
    args = sys.argv[1:]
    main(args)


if __name__ == '__main__':
    run()
