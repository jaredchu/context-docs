import pathlib,json,os
p=pathlib.Path(__file__).parent
r=p.parent
result={'fixture_read':(p/'project/README.md').read_text()=='# Synthetic route control\n\nRead this fixture without changing it.\n'}
(p/'project/owned-write.txt').write_text('owned scratch write\n')
result['owned_write']=(p/'project/owned-write.txt').read_text()=='owned scratch write\n'
for label,target in [('sibling_guard',r/'guard/sentinel.txt'),('frozen_package',p/'project/plugins/context-docs/plugin.json')]:
 try:
  fd=os.open(str(target),os.O_WRONLY|os.O_APPEND);os.close(fd);result[label+'_write_denied']=False
 except PermissionError:result[label+'_write_denied']=True
try:
 pathlib.Path('<real-project>/README.md').read_bytes();result['real_project_read_denied']=False
except PermissionError:result['real_project_read_denied']=True
print(json.dumps(result,sort_keys=True))
if not all(result.values()):raise SystemExit(2)
