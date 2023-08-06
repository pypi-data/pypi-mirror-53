## Controller Python Script "blaccount_taxgroups_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id='',ids=[],taxgroups=()
##title=edit account tax groups
##
REQUEST=context.REQUEST
 
if REQUEST.has_key('form.button.Edit'):
    context.manage_editTaxGroups(taxgroups)

context.plone_utils.addPortalMessage('Tax groups Updated')

return state

