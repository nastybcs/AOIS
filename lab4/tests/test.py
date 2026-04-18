import unittest
from models import calculate_v
from hash_table import GrammarHashTable


class TestGrammarHashTable(unittest.TestCase):
    def setUp(self):

        self.ht = GrammarHashTable(20)

    def test_calculate_v(self):

        self.assertEqual(calculate_v("аб"), 1)

        self.assertEqual(calculate_v("АБ"), 1)

        self.assertEqual(calculate_v("а"), 0)

    def test_insert_and_search(self):

        self.ht.insert("Глагол", "Действие")
        row = self.ht.search("Глагол")
        self.assertIsNotNone(row)
        self.assertEqual(row.pi, "Действие")
        self.assertEqual(row.u, 1)

    def test_duplicate_insert(self):

        self.ht.insert("Союз", "Часть речи")
        success, msg = self.ht.insert("Союз", "Другое описание")
        self.assertFalse(success)
        self.assertEqual(msg, "Слово уже есть в таблице")

    def test_collision_chaining(self):

        self.ht.insert("Сказуемое", "1")
        self.ht.insert("Причастие", "2")

        row1 = self.ht.search("Сказуемое")
        row2 = self.ht.search("Причастие")

        self.assertEqual(row1.c, 1)
        self.assertEqual(row1.t, 0)
        self.assertEqual(row1.p0, row2.index)

    def test_delete_case_a(self):

        self.ht.insert("Наречие", "Признак")
        idx = self.ht.search("Наречие").index
        self.ht.delete("Наречие")
        self.assertEqual(self.ht.table[idx].u, 0)

    def test_delete_case_vg(self):

        self.ht.insert("Сказуемое", "Первый")
        self.ht.insert("Причастие", "Второй")

        self.ht.delete("Сказуемое")

        row = self.ht.table[5]
        self.assertEqual(row.id, "Причастие")
        self.assertEqual(row.u, 1)
        self.assertEqual(row.t, 1)

    def test_load_factor(self):

        self.assertEqual(self.ht.get_load_factor(), 0.0)
        self.ht.insert("Слово1", "Д")
        self.ht.insert("Слово2", "Д")
        self.assertEqual(self.ht.get_load_factor(), 2 / 20)

    def test_table_overflow(self):

        small_ht = GrammarHashTable(2)
        small_ht.insert("А", "1")
        small_ht.insert("Б", "2")
        success, msg = small_ht.insert("В", "3")
        self.assertFalse(success)
        self.assertEqual(msg, "Таблица переполнена")


if __name__ == "__main__":
    unittest.main()
