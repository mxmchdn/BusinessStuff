from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from .models import Post

from subprocess import run, PIPE
import sys, os, csv

# Create your views here.
def home(request):
	return render(request, 'Interface/base.html')

@login_required
def service(request):
	return render(request, 'Interface/service.html', {'title': 'Services'})

@login_required
def checktva(request):
	context = {
		'posts': Post.objects.all(),
		'title': 'Check TVA'
	}
	return render('Interface/checktva.html', context)

class PostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'Interface/checktva.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
					ordering = self.request.GET.get('date_posted', '-date_posted')
					file_list = Post.objects.filter(author=self.request.user).order_by(ordering)
					return file_list

class PostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Post

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
	
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['name', 'description', 'file', 'service']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['name', 'description', 'file', 'service']
	template_name = 'Interface/post_update.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/service/'

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

@login_required
def about(request):
	return render(request, 'Interface/about.html', {'title': 'About'})

def clean(value):
	value = value.decode('utf-8')
	value = value.replace('\r', '')
	value = value.replace('\n', '')
	value = value.replace(' ', '')
	return value

def default_creation():
	default = open('media/default.csv', "w")
	default.write('Name;TVA_Number;TVA_Name;TVA_Address;TVA_CP_Country;Exist;Request_Date')
	default.close()

def extract_line_out(dict, path_file):
	with open(path_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';')
		for row in reader:
			dict['content'].append({
				'Name': row['Name'],
				'TVA_Number': row['TVA_Number'],
				'TVA_Name': row['TVA_Name'],
				'TVA_Address': row['TVA_Address'],
				'TVA_CP_Country': row['TVA_CP_Country'],
				'Exist': row['Exist'],
			})
	return dict

def extract_line_in(dict, path_file):
	with open(path_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';')
		for row in reader:
			dict['content'].append({
				'Name': row['Name'],
				'TVA': row['VAT'],
			})
	return dict

@login_required
def execute(request):
	inp = str(request.POST.get('path'))
	context = {
		'title': 'Execution',
		'output': '',
		'content':[]
	}
	if inp != 'None':
		inp_disas = inp.split('/')
		inp_folder = inp_disas[0]
		inp_file = inp_disas[1]
		list_inp = os.listdir('media/tables_inputs')
	else:
		inp_folder = ''
		inp_file = ''
		list_inp = []

	if inp == 'None':
		context['output'] = 'Not Executed'
	elif inp_folder != 'tables_inputs':
		context['output'] = 'Only input file are executable!'
	elif not inp_file in list_inp:
		context['output'] = 'The file does not exist!'
	elif inp_file.endswith('.txt') or inp_file.endswith('.csv'):
		post = Post.objects.get(file=inp)
		if post.author != request.user:
			context['output'] = 'You are not authorize to execute this file!'
		elif request.user.profile.execution_left != 0:
			request.user.profile.execution_left -= 1
			request.user.profile.save()
			exe = run([sys.executable, 'CheckVatAPI.py', 'media/' + inp], shell=False, stdout=PIPE)
			out = clean(exe.stdout).split('/')
			if post.output_file == 'default.csv':
				post.output_file.delete()
				default_creation()
				post.output_file = out[1] + '/' + out[2]
				post.save()
			context['output'] = 'File content is:'
			extract_line_out(context, out[0] + '/' + out[1] + '/' + out[2])
		else:
			context['output'] = 'You have no more execution left!'

	return render(request, 'Interface/execute.html', context)

@login_required
def visualization(request):
	inp = str(request.POST.get('path'))
	context = {
		'title': 'Execution',
		'output': '',
		'content':[],
		'type': ''
	}
	if inp != 'None':
		inp_disas = inp.split('/')
		inp_folder = inp_disas[0]
		inp_file = inp_disas[1]
		list_inp = os.listdir('media/tables_inputs')
		list_out = os.listdir('media/tables_outputs')
	else:
		inp_folder = ''
		inp_file = ''
		list_inp = []
		list_out = []
	if inp == 'None':
		context['output'] = 'No file selected!'
	elif inp_folder != 'tables_outputs' and inp_folder != 'tables_inputs':
		context['output'] = 'Path file not respected!'
	elif not inp_file in list_inp and not inp_file in list_out:
		context['output'] = 'Your file does not exist!'
	else:
		if inp_folder == 'tables_outputs':
			context['type'] = 'out'
			post = Post.objects.get(output_file=inp)
		else:
			context['type'] = 'in'
			post = Post.objects.get(file=inp)
		if post.author != request.user:
			context['output'] = 'You are not authorize to execute this file!'
		else:
			context['output'] = 'This is it!'
			if context['type'] == 'out':
				extract_line_out(context, 'media/' + inp)
			else:
				extract_line_in(context, 'media/' + inp)
	return render(request, 'Interface/visualization.html', context)