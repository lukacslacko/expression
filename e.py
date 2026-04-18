import cmath

class Node:
    def __init__(self, x, y):
        assert x == 1 or isinstance(x, Node)
        assert y == 1 or isinstance(y, Node)
        self.left = x
        self.right = y

    def __str__(self):
        return "E(" + str(self.left) + "," + str(self.right) + ")"

    def eval(self):
        x = 1 if self.left == 1 else self.left.eval()
        y = 1 if self.right == 1 else self.right.eval()
        return cmath.exp(x) - cmath.log(y)

    def ascii(self):
        def collides(a, b):
            for ca, cb in zip(a, b):
                if ca != ' ' and cb != ' ':
                    return True
            return False

        def overlay(a, b):
            n = max(len(a), len(b))
            a = a.ljust(n)
            b = b.ljust(n)
            return ''.join(ca if cb == ' ' else cb for ca, cb in zip(a, b))

        def render(node):
            if node == 1:
                return [""]
            left = render(node.left)
            head = "┬─" if node.left == 1 else "┬──" + left[0]
            if node.right == 1:
                out = [head]
                out.extend("   " + l for l in left[1:])
                return out
            right = render(node.right)
            h_l = len(left)
            h_r = len(right)

            def left_line(i, k):
                if i == 0:
                    return head
                if i < k:
                    return "│  " + left[i]
                return "   " + left[i]

            def right_line(j):
                if j == 0:
                    return "╰──" + right[0]
                return "   " + right[j]

            chosen_k = h_l
            for k in range(1, h_l + 1):
                ok = True
                for j in range(h_r):
                    i = k + j
                    if i < h_l and collides(left_line(i, k), right_line(j)):
                        ok = False
                        break
                if ok:
                    chosen_k = k
                    break

            total = max(h_l, chosen_k + h_r)
            out = [left_line(0, chosen_k)]
            for i in range(1, total):
                pieces = []
                if i < h_l:
                    pieces.append(left_line(i, chosen_k))
                if chosen_k <= i < chosen_k + h_r:
                    pieces.append(right_line(i - chosen_k))
                if len(pieces) == 1:
                    out.append(pieces[0])
                else:
                    out.append(overlay(pieces[0], pieces[1]))
            return out

        return "\n".join(render(self))


def E(x, y):
    return Node(x, y)


def exp(x):
    return E(x, 1)


def e():
    return exp(1)


def zero():
    return E(1, exp(e()))


def one_minus_x(x):
    return E(zero(), exp(x))


def e_per_x(x):
    return exp(E(zero(), x))


def one_per_x(x):
    return one_minus_x(e_per_x(E(1, exp(e_per_x(one_minus_x(x))))))


def ln(x):
    return one_minus_x(E(zero(), x))


def x_per_y(x, y):
    return exp(E(ln(ln(x)), y))


def x_times_y(x, y):
    return x_per_y(x, one_per_x(y))


def x_plus_y(x, y):
    return ln(x_times_y(exp(x), exp(y)))


def two():
    return x_plus_y(1, 1)


def sqrt(x):
    return exp(x_per_y(ln(x), two()))

def minus_one():
    return one_minus_x(two())
    
def i():
    return sqrt(minus_one())
    
def i_pi():
    return ln(minus_one())
    
def pi():
    return x_per_y(i_pi(), i())

a = pi()
print(a)
print(a.eval())
print(a.ascii())
