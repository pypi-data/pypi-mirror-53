class Person
  def initialize(@name : String)
  end

  def greet
    puts "Hi, I'm #{@name}"
  end
end

class Employee < Person
end

employee = Employee.new "John"
employee.greet         # => "Hi, I'm John"
employee.is_a?(Person) # => true

@[Link("m")]
lib C
  # In C: double cos(double x)
  fun cos(value : Float64) : Float64
end

C.cos(1.5_f64) # => 0.0707372

s = uninitialized String
s = <<-'STR'
\hello\world
\hello\world
STR