# Requirements
1. Python 3
2. GitPython

        pip install gitpython
3. Requests

        pip install requests
# Usage
1. Fill out all variables in settings.conf
A sample is shown in settings_sample.conf

	username: Your Prisma Cloud Access Key
	password: Your Prisma Cloud Secret Key
	apiBase: The link you use to access Prisma Cloud, e.g. app.prismacloud.io
	accessToken: A GitHub personal access token - should be given full repo permissions.
	gitUser: Your GitHub username
	repoPath: A path to an empty folder on your computer that will contain the local git repository
	remoteUrl: After creating an empty repo on GitHub, copy its HTTPS url, e.g. https://github.com/abcd/repository.git

2. Run the program with

        python3 runner.py
