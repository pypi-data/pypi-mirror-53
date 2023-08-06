## Controller Python Script "blaccount_email_statement"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=email,message='',effective=None
##title=email a statement
##

try:
    recipients = context.manage_emailStatement(email, message, effective or DateTime())
except ValueError as e:
    context.plone_utils.addPortalMessage("Invalid Emails: %s" % str(e))
    return state.set(status='failure')
    
context.plone_utils.addPortalMessage("Statement emailed to %s" % ', '.join(recipients))
return state.set(status='success')
