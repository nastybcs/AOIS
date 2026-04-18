from models import HashRow, calculate_v


class GrammarHashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [HashRow(i) for i in range(size)]

    def h1(self, v):

        return v % self.size

    def h2(self, v):

        return 1 + (v % (self.size - 1))

    def insert(self, word, definition):
        v = calculate_v(word)
        h = self.h1(v)

        if self.search(word) is not None:
            return False, "Слово уже есть в таблице"

        if self.table[h].u == 0:
            self._fill_row(h, word, definition)
            return True, h

        self.table[h].c = 1
        curr = h
        step = self.h2(v)

        for i in range(1, self.size):
            next_idx = (h + i * step) % self.size
            if self.table[next_idx].u == 0:
                self.table[curr].t = 0
                self.table[curr].p0 = next_idx
                self._fill_row(next_idx, word, definition)
                return True, next_idx
            curr = next_idx

        return False, "Таблица переполнена"

    def _fill_row(self, idx, word, definition):
        row = self.table[idx]
        row.id = word
        row.u = 1
        row.t = 1
        row.d = 0
        row.p0 = idx
        row.pi = definition

    def search(self, word):
        v = calculate_v(word)
        h = self.h1(v)
        curr = h
        step = self.h2(v)

        for _ in range(self.size):
            row = self.table[curr]
            if row.u == 1 and row.id == word and row.d == 0:
                return row
            if row.t == 1 and row.c == 0:
                break
            curr = (curr + step) % self.size
        return None

    def delete(self, word):

        row = self.search(word)
        if not row:
            return False

        row.d = 1
        idx = row.index

        if row.t == 1 and row.c == 0:
            row.u = 0
            row.d = 0
            return True

        if row.t == 1:
            for r in self.table:
                if r.u == 1 and r.p0 == idx and r.index != idx:
                    r.t = 1
                    r.p0 = r.index
                    break
            row.u = 0
            row.d = 0
            return True
        next_idx = row.p0
        next_row = self.table[next_idx]

        row.id = next_row.id
        row.pi = next_row.pi
        row.p0 = next_row.p0
        row.t = next_row.t
        row.d = 0
        next_row.u = 0
        next_row.id = ""
        next_row.pi = ""

        return True

    def get_load_factor(self):

        occupied = sum(1 for r in self.table if r.u == 1)
        return occupied / self.size

    def interactive_add(self):

        word = input("Введите термин: ")
        definition = input("Введите определение: ")

        success, res = self.insert(word, definition)
        if success:
            print(f"Успешно добавлено в ячейку {res}")
        else:
            print(f"Ошибка: {res}")

    def interactive_delete(self):

        word = input("Введите слово для удаления: ")
        v = calculate_v(word)
        h = self.h1(v)

        row = self.search(word)
        if not row:
            print("Запись не найдена")
            return

        row.d = 1
        idx = row.index

        if row.t == 1 and row.p0 == idx:
            row.u = 0
            print(f"Удалена одиночная строка {idx}")

        elif row.t == 1 and row.p0 != idx:
            for prev_row in self.table:
                if prev_row.u == 1 and prev_row.p0 == idx and prev_row.index != idx:
                    prev_row.t = 1
                    prev_row.p0 = prev_row.index
                    break
            row.u = 0
            print(f"Удален конец цепочки (ячейка {idx})")

        else:
            next_idx = row.p0
            next_row = self.table[next_idx]

            row.id = next_row.id
            row.pi = next_row.pi
            row.p0 = next_row.p0
            row.t = next_row.t
            row.d = 0

            next_row.u = 0
            print(
                f"Строка {idx} обновлена данными из {next_idx}, ячейка {next_idx} освобождена"
            )
