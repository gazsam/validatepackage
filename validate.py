# crude validation for DITA packages
# python validate.py html-import__hdp__2.0.tgz
# ^^ the first (required) parameter is the name of the package you want to inspect.  The tarball must be in same directory as script

from lxml import etree
from io import StringIO, BytesIO
import sys, re, tarfile

def packagename():
	package = open(sys.argv[1])
	first_part = re.escape('html-import__')
	middle_part = re.escape('__')
	last_part = re.escape('.tgz')
	m = re.search(first_part + '.+' + middle_part + '\d+\.\d+' + last_part, package.name)
	if m:
		print 'Filename: pass'
	else:
		print 'Filename: fail'
	package.close()
	#tree = etree.parse(filename)
def has_import_xml():
	#try:
	package = tarfile.open(sys.argv[1], mode="r:gz")
	filename = './html-import.xml'
	try:
		f = package.extractfile(filename)
	except KeyError:
		print 'html-import exists: fail- Did not find %s in tar archive' % filename
	else:
		print 'html-import exists: pass'
	package.close()
	#except:
		#print 'Has XML: fail- not valid tarball'
def valid_import_xml():
	package = tarfile.open(sys.argv[1], mode="r:gz")
	filename = './html-import.xml'
	try:
		f = package.extractfile(filename)
	except KeyError:
		print 'html-import parse: fail- Did not find %s in tar archive' % filename
	try:
		tree = etree.parse(f)
		print 'html-import parse: pass- valid XML'
	except:
		print 'html-import parse: fail- does not appear to be valid xml'

def html_import_node():
	package = tarfile.open(sys.argv[1], mode="r:gz")
	filename = './html-import.xml'
	try:
		f = package.extractfile(filename)
	except KeyError:
		print 'html-import-node parse: fail- Did not find %s in tar archive' % filename
	try:
		tree = etree.parse(f)
		root = tree.getroot()
		if root.tag == 'html-import':
			print 'html-import-node parse: pass- root element is html-import'
	except:
		print 'html-import-node parse: fail- does not appear to have correct root node'
	package.close()

def html_import_metadata():
	package = tarfile.open(sys.argv[1], mode="r:gz")
	filename = './html-import.xml'
	try:
		f = package.extractfile(filename)
	except KeyError:
		print 'html-import-metadata parse: fail- Did not find %s in tar archive' % filename
	try:
		tree = etree.parse(f)
		root = tree.getroot()
		if root.tag == 'html-import':
			#Check to see if it has a single metadata child
			children = root.getchildren()
			metadata = None
			count = 0
			for child in children:
				if child.tag == 'metadata':
					count += 1
					metadata = child
			if count != 1 or metadata is None:
				print 'html-import-metadata: fail- wrong number of metadata nodes'
			else:
				metadata_children = metadata.getchildren()
				tags = []
				values = []				
				for mc in metadata_children:
					tags.append(mc.tag)
					values.append(mc.text)
				first_part = re.escape('html-import__')
				middle_part = re.escape('__')
				last_part = re.escape('.tgz')
				m = re.match(first_part + '(.+)' + middle_part + '(\d+\.\d+)' + last_part, sys.argv[1])
				package_key = m.group(1)
				package_version = m.group(2)
				if (len(metadata_children) == 2) and (tags[0] == 'package-key') and (tags[1] == 'package-version') and (values[0]==package_key) and (values[1]==package_version):
					print 'html-import-metadata: pass- metadata node exists and has the right children with valid values' 
				else:
					print 'html-import-metadata: fail- does not appear to have correct root node or metadata child'
		else:
			print 'html-import-metadata: fail- wrong root node'

	except:
		print 'html-import-metadata: fail- does not appear to have correct root node or metadata child'
	package.close()

packagename()
has_import_xml()
valid_import_xml()
html_import_node()
html_import_metadata()

