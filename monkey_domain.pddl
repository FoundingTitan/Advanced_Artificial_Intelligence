
(define (domain monkey_domain)

  (:requirements :strips)

  (:predicates
   (pushable ?thing) (climbable ?thing) (graspable ?thing)
   (at ?thing ?loc) (height ?thing ?measure) (notequal ?loc ?loc) (have ?thing ?thing) (on ?thing ?thing)
  )

  (:constants Monkey Box Banana High Low A B C)

  (:action Go
    :parameters (?loc1 ?loc2)
    :precondition (and (at Monkey ?loc1) (height Monkey Low) (notequal ?loc1 ?loc2))
    :effect (and (at Monkey ?loc2) (not (at Monkey ?loc1)))
  )

  (:action Push
    :parameters (?loc1 ?loc2)
    :precondition (and (at Monkey ?loc1) (height Monkey Low) (at Box ?loc1) (pushable Box) (height Box Low) (notequal ?loc1 ?loc2)) 
    :effect (and (at Box ?loc2) (at Monkey ?loc2) (not (at Box ?loc1)) (not (at Monkey ?loc1)))
  )

  (:action ClimbUp
    :parameters (?loc1)
    :precondition (and (at Monkey ?loc1) (height Monkey Low) (at Box ?loc1) (climbable Box) (height Box Low))
    :effect (and (on Monkey Box) (not (height Monkey Low)) (height Monkey High))
  )

  (:action ClimbDown  
    :parameters (?loc1)
    :precondition (and (at Monkey ?loc1) (at Box ?loc1) (on Monkey Box) (not (height Monkey Low)) (height Monkey High))
    :effect (and (not (on Monkey Box)) (height Monkey Low) (not (height Monkey High)))
  )

  (:action Grasp
    :parameters (?loc1)
    :precondition (and (at Monkey ?loc1) (height Monkey High) (at Banana ?loc1) (graspable Banana) (height Banana High))
    :effect (and (have Monkey Banana) (not (height Banana High)))
  )

  (:action Ungrasp
    :parameters (?loc1)
    :precondition (and (have Monkey Banana) (not (height Banana High)))
    :effect (and (at Monkey ?loc1) (height Monkey Low) (at Banana ?loc1) (height Banana High) (not (have Monkey Banana)))
  )
  )

