program main
  use xx_kinds
  use xx_prospino_subroutine
  implicit none

  integer                              :: inlo,isq_ng_in,icoll_in,i_error_in,ipart1_in,ipart2_in,isquark1_in,isquark2_in
  real(kind=double)                    :: energy_in
  logical                              :: lfinal
  character(len=2)                     :: final_state_in
  integer, dimension (4)               :: i1 = [1, 2, 5, 7]
  character(len=100)                   :: filename,energystr
  integer                              :: icount,jcount


!----------------------------------------------------------------------------
  inlo = 1       ! specify LO only[0] or complete NLO (slower)[1]           !
!                ! results: LO     - LO, degenerate squarks, decoupling on  !
!                !          NLO    - NLO, degenerate squarks, decoupling on !
!                !          LO_ms  - LO, free squark masses, decoupling off !
!                !          NLO_ms - NLO, free squark masses, scaled        !
!                ! all numerical errors (hopefully) better than 1%          !
!                ! follow Vegas iteration on screen to check                !
!----------------------------------------------------------------------------

!----------------------------------------------------------------------------
  isq_ng_in = 0     ! specify degenerate [0] or free [1] squark masses      !
                    ! [0] means Prospino2.0 with average squark masses      !
                    ! [0] invalidates isquark_in switch                     !
!----------------------------------------------------------------------------

!----------------------------------------------------------------------------
  icoll_in = 1      ! collider : tevatron[0], lhc[1]                        !
!----------------------------------------------------------------------------

!----------------------------------------------------------------------------
  i_error_in = 0    ! with central scale [0] or scale variation [1]         !
!----------------------------------------------------------------------------

!----------------------------------------------------------------------------
  final_state_in = 'nn'                                                     !
!                                                                           !
!                   nn     neutralino/chargino pair combinations            !
!  ipart1_in   = 1,2,3,4  neutralinos                                       !
!                5,6      positive charge charginos                         !
!                7,8      negative charge charginos                         !
!  ipart2_in the same                                                       !
!      chargino+ and chargino- different processes                          !
!----------------------------------------------------------------------------

isquark1_in = 0                                                           !
isquark2_in = 0


  if (COMMAND_ARGUMENT_COUNT().NE.2) then
    write(*,*) 'ERROR, TWO COMMAND-LINE ARGUMENTS (FILENAME, SQRTS) REQUIRED, STOPPING'
    stop
  end if
  CALL GET_COMMAND_ARGUMENT(1,filename)   !first, read input filename
  CALL GET_COMMAND_ARGUMENT(2,energystr)   !then read energy
  read(energystr,*) energy_in

  call MYPROSPINO_OPEN_CLOSE(0,filename)                                                            ! open all input/output files

  do icount = 1,4,1
    do jcount = 1,4,1
      if (icount > jcount) then
         continue
      end if

      ipart1_in = i1(icount)
      ipart2_in = i1(jcount)

      call PROSPINO_CHECK_HIGGS(final_state_in)                                              ! lock Higgs final states
      call PROSPINO_CHECK_FS(final_state_in,ipart1_in,ipart2_in,lfinal)                      ! check final state
      if (.not. lfinal ) then
         continue
      end if

      call PROSPINO(inlo,isq_ng_in,icoll_in,energy_in,i_error_in,final_state_in,ipart1_in,ipart2_in,isquark1_in,isquark2_in)
    end do
  end do

  call MYPROSPINO_OPEN_CLOSE(1,filename)                                                            ! close all input/output files

end program main
