@IF DEFINED PYTHON (@setlocal enableextensions & %PYTHON% -u -x %~f0 %* & goto :EOF) ELSE (@setlocal enableextensions & python.exe -u -x %~f0 %* & goto :EOF)
#!python.exe
# EASY-INSTALL-SCRIPT: 'md-protobuf==0.0.1','protoc-gen-md'
__requires__ = 'md-protobuf==0.0.1'
import sys
try:
  import pkg_resources
  pkg_resources.run_script('md-protobuf==0.0.1', 'protoc-gen-md')
except Exception as e:
  import sys
  if type(e).__name__ == 'DistributionNotFound':
    from os.path import dirname, realpath
    path = dirname(realpath(__file__))
    sys.path.append(path)
    try:
      filename = '%s/protoc-gen-md'%path
      exec(compile(open(filename, 'r').read(), filename, 'exec'))
    except Exception as e:
      sys.stderr.write('Failed to generate -%s-%s'%(type(e).__name__, e))
      import traceback
      print(traceback.format_exc())
      sys.exit(1)
  else:
    sys.stderr.write('Failed to generate -%s-%s'%(type(e).__name__, e))
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
