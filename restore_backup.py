 # -*- coding: utf-8 -*-
import pc_lib

import json
import glob
cfg=pc_lib.config
policy_files=glob.glob(cfg['repoPath']+'*')
policies_in_prisma=pc_lib.api_policy_list_get({'policy.policyMode':'custom'})['data']

name_dict=dict() #stores current id for all policies, in case of change
for policy in policies_in_prisma:
    name_dict[policy['name']]=policy['policyId']

policy_backups=list()
for f in policy_files: #load all policy backups
    tmp=json.load(open(f,'r'))
    policy_backups.append(tmp)
    
    
for policy in policy_backups:
    policy.pop('policyId',None)
    if policy['name'] in name_dict:
        #If policy exists, update to backup status
        print('Updating %s'%(policy['name']))
        pc_lib.api_policy_update(name_dict[policy['name']],policy)
        continue
    else:
        #If policy not in Prisma, readd
        print('Adding %s'%(policy['name']))
        pc_lib.api_policy_add(policy)
        