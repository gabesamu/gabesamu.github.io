---
title: 'Sicp Section 1.1 Exercises'
pubDate: 2023-07-13
description: 'Sicp section 1.1 - The Elements of Programming solutions and thoughts.'
tags: ["skill-up", "sicp", "book", "notes"]
---

## Exercise 1.1:

Below is a sequence of expressions.
What is the result printed by the interpreter in response to each expression?
Assume that the sequence is to be evaluated in the order in which it is presented.

---

### Answer:

``` scheme
10
Value: 10

(+ 5 3 4)
Value: 12

(- 9 1)
Value: 8

(/ 6 2)
Value: 3

(+ (* 2 4) (- 4 6))
Value: 6

(define a 3)
(define b (+ a 1))
(+ a b (* a b))
Value: 19

(= a b)
Value: #f

(if (and (> b a) (< b (* a b)))
    b
    a)
Value: 4

(cond ((= a 4) 6)
      ((= b 4) (+ 6 7 a))
      (else 25))
Value: 16

(+ 2 (if (> b a) b a))
Value: 6

(* (cond ((> a b) a)
         ((< a b) b)
         (else -1))
   (+ a 1))
Value: 16
```

<br>
<br>
<br>

## Exercise 1.2

Translate the following expression into prefix form:
>
>`5 + 4 + (2 - (3 - (6 + 4/5))) / 3(6-2)(2-7)`

---

### Answer:

``` scheme
(/ (+ 5 4 (- 2 (- 3 (+ 6 (/ 4 5)))))
   (* 3 (- 6 2) (- 2 7)))
```

<br>
<br>
<br>

## Exercise 1.3

Define a procedure that takes three numbers as arguments and returns the sum of the squares of the two larger numbers.

---

### Answer:

``` scheme
(define (square x) (* x x))

(define (sum-of-squares x y) (+ (square x) (square y)))

(define (sum-of-larger-squares x y z)
  (cond ((and (<= x y) (<= x z)) (sum-of-squares y z))
        ((and (<= y x) (<= y z)) (sum-of-squares x z))
        (else (sum-of-squares x y))))


(sum-of-larger-squares 4 3 2)
Value: 25
```

<br>
<br>
<br>

## Exercise 1.4

Observe that our model of evaluation allows for combinations whose operators are compound expressions.
Use this observation to describe the behavior of the following procedure:
``` scheme
(define (a-plus-abs-b a b)
    ((if (> b 0) + -) a b))
```

---

### Answer:

The operator to be used depends on the evaluation of the if predicate.
If b is greater than 0, the operator will be `+`, otherwise it will be `-` .
This ensures that a will always be added with the absolute value of b.

<br>
<br>
<br>

## Exercise 1.5:


Ben Bitdiddle has invented a test to determine whether the interpreter he
is faced with is using applicative-order evaluation or normal-order evaluation.
He defines the following two procedures:
``` scheme
(define (p) (p))

(define (test x y)
    (if (= x 0)
        0
        y))
```
Then he evaluates the expression:
``` scheme
(test 0 (p))
```
What behavior will Ben observe with an interpreter that uses applicative-order evaluation?
What behavior will he observe with an interpreter that uses normal-order evaluation?
Explain your answer. (Assume that the evaluation rule for the special form (if) is the same whether
                      the interpreter is using normal or applicative order: The predicate expression is evaluated first,
                      and the result determines whether to evaluate the consequent or the alternative expression.


---

### Answer:

Given an interpreter using applicative-order eval, The expression will cause and infinite loop.
This behavior is due to the fact that arguments will be evaluated before the procedure is ran.
This means procedure (p) is ran which kicks off the loop.

Given an interpreter using normal-order eval, This expression will return 0.
This completes without issue because the argument are not evaluated before procedure call,
but evaluation is delayed until the value is needed. This means procedure (p) is never actually,
called due to the if statement in (test). Given any value for x other than 0, this mode will also infinite loop.
