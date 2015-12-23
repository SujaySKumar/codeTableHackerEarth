from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse

from parameters import SupportedLanguages
from parameters import RunAPIParameters

from api_handlers import HackerEarthAPI

@csrf_exempt
def index(request):
	template = loader.get_template('initial/index.html')
	
	return HttpResponse(template.render())

def sujay(code, language, inp=None):
	client_secret = '0a7f0101e5cc06e4417a3addeb76164680ac83a4'

	#source = open('test_source.py', 'r').read()
	source=code
	#lang = SupportedLanguages.PYTHON
	lang = language
	compressed = 1
	html = 0
	params = RunAPIParameters(
        client_secret=client_secret, source=source,
        lang=lang, compressed=compressed, html=html, program_input=inp)

	api = HackerEarthAPI(params)

	print 'Compiling code..'
	r = api.compile()
	print r.__dict__
	if r.__dict__.get('compile_status')!='OK':
		return r.__dict__.get('compile_status')

	print '\nRunning code...'
	r = api.run()
	print r.__dict__
	output = r.__dict__.get('output')

	print '\nRun Output:'
	print output
	return output


@csrf_exempt
def submitCode(request):
	code = request.POST['code']
	lang = request.POST['lang']
	inp = ''
	if request.POST.get('checkInput'):
		inp = request.POST['customInput']
		print "INside Herr"
	print inp
	print type(inp)
	#print code
	output = sujay(code, lang, str(inp))
	template = loader.get_template('initial/index.html')
	context = RequestContext(request, {
        'output': output,
    })
	return HttpResponse(template.render(context))

