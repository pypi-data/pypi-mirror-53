## Controller Python Script "bltransaction_add_entries"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=effective, addentries=[], editentries=[], title='', description='', tags=[], notes=''
##title=add entries to a transaction
##
from Products.BastionBanking.ZCurrency import ZCurrency
from Products.BastionLedger.utils import assert_currency

REQUEST = context.REQUEST

if REQUEST.has_key('form.button.EditEntries'):
    # make sure we can set/reset incomplete
    context.manage_unpost()
    context.manage_editEntries(editentries)
    context.plone_utils.addPortalMessage('Updated Entries')
    return state.set(context=context)

if context.modifiable():

    if context.status() in ('posted',):
        context.manage_unpost()

    id = context.getId()
    new_context = context.portal_factory.doCreate(context, id)

    new_context.editProperties(title, description, effective, tags, notes)
    
    # don't do entries with blank amounts ...
    for entry in filter(lambda x: getattr(x, 'amount', None), addentries):
        try:
	    assert_currency(entry.amount)
        except:
            entry.amount = ZCurrency(entry.amount)

        # be paranoid in determining debit/credit values ...
        if entry.get('credit', False):
            entry.amount = -abs(entry.amount)
        else:
            entry.amount = abs(entry.amount)

	new_context.createEntry(entry.account, entry.amount, entry.title, entry.get('subsidiary', False))

context.plone_utils.addPortalMessage('Added Entries')
return state.set(context=new_context)

