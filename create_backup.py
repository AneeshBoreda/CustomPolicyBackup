 # -*- coding: utf-8 -*-
import pc_lib
from git import *
import os
import json
from datetime import datetime


policies=pc_lib.api_policy_list_get({'policy.policyMode':'custom'})['data']
cfg=pc_lib.config
remote_url=cfg['remoteUrl'].replace('https://','https://%s:%s@'%(cfg['gitUser'],cfg['accessToken']),1)

print('Repo folder: %s'%(os.path.abspath(cfg['repoPath'])))



origin=None
repo = Repo.init(cfg['repoPath'])
if len(repo.remotes)==0:
    origin = repo.create_remote('origin', url=remote_url)
    print('Created remote origin')
else:
    origin=repo.remote('origin')
    print('Remote already exists, skipping')

print('Getting saved search information.')
for policy in policies:
    
    if 'savedSearch' in policy['rule']['parameters']:
        if policy['rule']['parameters']['savedSearch']=='true':
            searchId=policy['rule']['criteria']
            if type(searchId)==str:
                searchData=pc_lib.api_search_get(searchId)['data']
                policy['searchData']=searchData
    json.dump(policy,open(cfg['repoPath']+policy['policyId']+'.json','w'),indent=3)
            
repo.git.add(A=True)
date_str = datetime.now().strftime("%b-%d-%Y %H:%M:%S")    
try:
    print('Committing with message: Prisma Cloud Policy Backup %s'%(date_str))
    repo.git.commit('-m', 'Prisma Cloud Policy Backup %s'%(date_str))    
except:
    print('No uncommitted changes found, skipping commit.')

print('Pushing to GitHub')
repo.git.push('-u',origin,'master')

    