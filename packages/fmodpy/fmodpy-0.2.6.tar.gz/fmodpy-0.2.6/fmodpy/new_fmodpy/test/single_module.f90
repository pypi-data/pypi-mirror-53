

! Documentation for the module "TEST" goes in a comment immediately
! before the module itself.
MODULE TEST

  ! Documentation for the function "ADD" goes immediately before the
  ! subroutine. This subroutine takes 3 arguments.
  SUBROUTINE ADD(A, B, C)
    REAL, INTENT(IN) :: A, B
    REAL, INTENT(OUT) :: C
    C = A + B
  END SUBROUTINE ADD

END MODULE TEST

