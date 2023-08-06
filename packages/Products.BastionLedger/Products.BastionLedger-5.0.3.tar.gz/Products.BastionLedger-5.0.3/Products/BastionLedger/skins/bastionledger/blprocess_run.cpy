## Controller Python Script "blprocess_run"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=run a process
##
REQUEST=context.REQUEST
 
kw = {}

for arg in context.parameterMap.propertyMap():
    if REQUEST.has_key(arg['id']):
        kw[arg['id']] = REQUEST[arg['id']]

context.manage_run(**kw)

context.plone_utils.addPortalMessage('Process completed')

return state
