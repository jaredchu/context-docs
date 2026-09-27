"""Pre-execution reference check, not a model trial. Requires Python >=3.10."""
import json
import sys
from pathlib import Path
from study import corpus

sys.dont_write_bytecode = True
corpus('click')  # Verify pin and unmodified tracked source first.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'.local/upstream-click/src'))
import click
from click.testing import CliRunner

@click.command()
@click.option('--level', is_flag=True, flag_value=10, type=int, envvar='LEVEL')
def command(level):
    click.echo(f'{level}:{type(level).__name__}')

rows=[]
for value in ['8','0']:
    result=CliRunner().invoke(command,env={'LEVEL':value})
    assert result.exit_code==0 and result.output=='10:int\n'
    rows.append(dict(environment={'LEVEL':value},output=result.output,exit_code=result.exit_code))
print(json.dumps(rows,indent=2))
