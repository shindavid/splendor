#include <initializer_list>

struct Foo {
  Foo(const std::initializer_list<int>& x, int y) {}
};

struct Bar {
  static constexpr const int x[] = {1,2,3};
};

int main() {
  Foo foo[] = {
    {{1,2}, 0},
    {{3,4}, 1}
  };
  return 0;
}
