__author__ = 'Tom'


def issue_comment(name, issue, id, to):
    body = "Hello, {name}.\n" \
           "There are one or more new comments in response to your reported issue: {issue}.\n\n" \
           "View the comments here: http://loka.minecraftarium.com/issue/{id}".format(name=name,
                                                                                      issue=issue,
                                                                                      id=id)
    send_message('Loka Issue - New Comment', body[to])


def issue_status_change(name, issue, id, status, to):
    body = "Hello, {name}.\n" \
           "The status of your reported issue, {issue}, has been changed to {status}.\n\n" \
           "You can view your issue here: http://loka.minecraftarium.com/issue/{id}".format(name=name,
                                                                                            status=status,
                                                                                            issue=issue,
                                                                                            id=id)
    send_message('Loka Issue - Status Updated', body, [to])


def issue_created(author, issue, id):
    body = "Hello!\n" \
           "A new issue has been created by {author}, {issue}\n\n" \
           "You can view the new issue here: http://loka.minecraftarium.com/issue/{id}".format(author=author,
                                                                                               issue=issue,
                                                                                               id=id)
    # mail_admins('Loka Issues - New Issue Created', body, fail_silently=True)


def send_message(subject, body, recipients):
    #TODO: Perhaps thread this at some point
    pass
    # send_mail(subject, body, 'lokaminecraft@gmail.com',
    #           [recipients], fail_silently=True)