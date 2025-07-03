program track_to_opal
    implicit none
    integer, parameter :: dp = selected_real_kind(15, 307)
    integer, parameter :: ncol = 6, nperrec = 4
    integer :: i, j, nread, ios
    real(dp), parameter :: c = 2.99792458e8_dp  ! speed of light [m/s]
    real(dp) :: record(ncol, nperrec)
    character(len=20) :: infile, outfile
    integer :: unit_in, unit_out
    real(dp) :: t

    infile = 'scratch.#02'
    outfile = 'beam.in'

    unit_in = 10
    unit_out = 20

    ! Open TRACK binary input file and OPAL ASCII output file
    open(unit=unit_in, file=infile, form='unformatted', access='sequential', action='read', status='old')
    open(unit=unit_out, file=outfile, status='replace', action='write')

    print *, 'Converting TRACK binary to OPAL .IN format...'
    nread = 0

    do
        read(unit_in, iostat=ios) record
        if (ios /= 0) exit

        do j = 1, nperrec
            t = record(5, j) / c  ! convert z [m] → t [s]
            write(unit_out,'(6ES15.6)') record(1,j), record(2,j), record(3,j), record(4,j), t, record(6,j)
            nread = nread + 1
        end do

        if (mod(nread, 400) == 0) then
            write(*,'(A,F6.2,A)') 'Progress: ', 100.0 * nread / 13608.0, ' %'
        end if
    end do

    close(unit_in)
    close(unit_out)

    print *, 'Done. Total particles written:', nread
end program track_to_opal

