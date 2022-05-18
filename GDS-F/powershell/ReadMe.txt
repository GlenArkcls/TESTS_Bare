This Powershell module makes available a commandlet called 'Write-WithColour' which just 
colourizes the output of running the GDS test system.

In a Powershell session, use Import-Module GDSAddOn to make it available.
If that fails, because it is not discoverable, then the whole directory (GDSAddOn) should be copied to
one of the module roots which can be found by typing $env:PSModulePath in the PS console.

Once available it is used by piping the output of the test system into it e.g.

c:>python core_tests.py -p56889 | Write-WithColour