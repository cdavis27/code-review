from rest_framework import serializers

from api.models import *

class ProjectSerializer(serializers.ModelSerializer):
	files = serializers.SerializerMethodField('_files')

	class Meta:
		model = Project

	def _files(self, object):
		if object.files:
			return FileSerializer(object.files.all(), many=True).data
		return None


class FileSerializer(serializers.ModelSerializer):
	snippet = serializers.SerializerMethodField('_snippet')
	contents = serializers.SerializerMethodField('_contents')
	language = serializers.SerializerMethodField('_language')
	comments = serializers.SerializerMethodField('_comments')

	class Meta:
		model = File

	def _snippet(self, object):
		N = 15 # number of lines to read
		with open(object.file.path) as myfile:
		    head = [next(myfile) for x in xrange(N)]
		return "".join(head)

	def _contents(self, object):
		contents = []
		with open(object.file.path) as myfile:
			for line in myfile:
				contents += line
		return "".join(contents)

	def _language(self, object):
		return LanguageSerializer(object.language).data

	def _comments(self, object):
		return CommentSerializer(object.comments, many=True).data


class LanguageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Language


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment 


class ReviewRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReviewRequest


