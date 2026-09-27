import unittest

from game.nightmare import NightmareDirector, ROLES


class NightmareDirectorTests(unittest.TestCase):
    def test_every_stage_has_one_of_each_route(self):
        n = NightmareDirector(seed=123)
        self.assertEqual(set(n.current.roles.values()), set(ROLES))
        self.assertEqual(set(n.current.roles.keys()), {"room_a", "room_b", "room_c"})

    def test_seed_is_deterministic(self):
        a = NightmareDirector(seed=99)
        b = NightmareDirector(seed=99)
        self.assertEqual(a.current.roles, b.current.roles)
        self.assertEqual(a.current.puzzle_id, b.current.puzzle_id)

    def test_puzzle_unlocks_next_route(self):
        n = NightmareDirector(seed=5)
        puzzle_slot = next(k for k, v in n.current.roles.items() if v == "puzzle")
        next_slot = next(k for k, v in n.current.roles.items() if v == "next")
        self.assertEqual(n.enter(puzzle_slot), "puzzle")
        self.assertEqual(n.enter(next_slot), "next_locked")
        self.assertTrue(n.solve())
        self.assertEqual(n.enter(next_slot), "next")

    def test_timer_expires(self):
        n = NightmareDirector(seed=1, duration=1.0)
        n.start()
        self.assertIsNone(n.update(0.5))
        self.assertEqual(n.update(0.5), "timeout")
        self.assertTrue(n.game_over)

    def test_advance_rerolls_stage(self):
        n = NightmareDirector(seed=42)
        old_stage = n.stage
        n.solve()
        n.advance()
        self.assertEqual(n.stage, old_stage + 1)
        self.assertEqual(set(n.current.roles.values()), set(ROLES))


if __name__ == "__main__":
    unittest.main()
