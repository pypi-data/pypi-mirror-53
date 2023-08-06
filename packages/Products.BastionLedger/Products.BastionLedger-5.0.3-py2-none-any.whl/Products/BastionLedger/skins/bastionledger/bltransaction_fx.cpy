## Controller Python Script "bltransaction_fx"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=editentries
##title=adjust fx
##
REQUEST=context.REQUEST

context.manage_bookFx(editentries)
context.plone_utils.addPortalMessage('Updated Transaction')

return state.set(context=context)

