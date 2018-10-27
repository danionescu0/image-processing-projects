from event.FacesFound import FacesFound


class MessageGenerator:
    def get_text(self, event: FacesFound):
        body = 'The following users have been found: '
        for user in event.users:
            if user.user_id is None:
                body += 'unknown, '
            else:
                body += user.user_name + ', '

        return body