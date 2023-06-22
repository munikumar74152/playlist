class Node:
    def __init__(self, user_id, song_id):
        self.user_id = user_id
        self.song_id = song_id
        self.prev = None
        self.next = None


class RecentlyPlayedStore:
    def __init__(self, initial_capacity):
        self.capacity = initial_capacity
        self.size = 0
        self.user_map = {}
        self.head = None
        self.tail = None

    def _update_node(self, node):
        if node == self.head:
            return

        # Remove the node from its current position
        node.prev.next = node.next

        if node == self.tail:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        # Move the node to the front of the list
        self._add_to_front(node)

    def _add_to_front(self, node):
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def _remove_least_recently_played(self):
        if self.tail is None:
            return

        # Remove the least recently played song from the store
        del self.user_map[self.tail.user_id]

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1

    def add_recently_played(self, user_id, song_id):
        # Check if the user is already in the store
        if user_id in self.user_map:
            node = self.user_map[user_id]
            self._update_node(node)  # Move the node to the front of the list
            node.song_id = song_id  # Update the song ID for the user
        else:
            # Create a new node for the recently played song
            node = Node(user_id, song_id)
            self.user_map[user_id] = node

            # Add the node to the front of the list
            self._add_to_front(node)

            # Check if the store has reached its capacity
            if self.size > self.capacity:
                self._remove_least_recently_played()
            else:
                self.size += 1

    def get_recently_played(self, user_id):
        if user_id in self.user_map:
            node = self.user_map[user_id]
            self._update_node(node)
            return node.song_id

r = RecentlyPlayedStore(3)

r.add_recently_played('U1', 'S1')
r.add_recently_played('U1', 'S2')
r.add_recently_played('U1', 'S3')
r.add_recently_played('U1', 'S4')

r.add_recently_played('U2', 'S3')
r.add_recently_played('U2', 'S4')
r.add_recently_played('U2', 'S1')
r.add_recently_played('U2', 'S2')

assert r.get_recently_played('U1') == 'S4'
assert r.get_recently_played('U2') == 'S2'
