import subprocess

"""
Wrap `ipcs -m` and `ipcrm -m <shm_id>` to remove all SHMs at a time
"""

if __name__ == '__main__':
    # Get living SHMs
    ipcs_m = subprocess.run(['ipcs', '-m'], stdout=subprocess.PIPE)
    shm_info = ipcs_m.stdout.decode('utf-8')

    print('Before ipcrm:')
    print(shm_info)

    # Cut in to lines and extract shm_ids
    shm_ids = []
    for line in shm_info.split('\n'):
        content = line.strip()
        if content == '':
            continue
        parts = list(filter(None, content.split(' ')))
        # Filter lines whose second column is not a number
        if not parts[1].isnumeric():
            continue
        shm_ids.append(parts[1])

    # Kill SHMs
    for shm_id in shm_ids:
        args = ['ipcrm', '-m', shm_id]
        subprocess.run(args)
        print('%s' % ' '.join(args))

    # Show result
    ipcs_m = subprocess.run(['ipcs', '-m'], stdout=subprocess.PIPE)
    result = ipcs_m.stdout.decode('utf-8')
    print('After ipcrm:')
    print(result)
