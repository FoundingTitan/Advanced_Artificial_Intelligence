(define (problem monkey_task)

  (:domain monkey_domain)
  
  (:objects thing loc1 loc2 measure)
  
  (:init (at Monkey A) (at Banana B) (at Box C) (height Monkey Low) (height Box Low) (height Banana High)
  	(pushable Box) (climbable Box) (graspable Banana) (notequal A B) (notequal A C) (notequal B A) (notequal B C)
  	(notequal C A) (notequal C B)
  )

  (:goal (have Monkey Banana)
  )
)
