program read_track_binary_progress
    implicit none
    integer, parameter :: dp = selected_real_kind(15, 307)
    integer, parameter :: ncol = 6, nperrec = 4
    integer :: i, j, nread, ios, total_records
    real(dp) :: record(ncol, nperrec)
    character(len=20) :: infile, outfile
    integer :: unit_in, unit_out
    real(dp) :: percent

    infile = 'scratch.#02'
    outfile = 'beam_out.dat'

    unit_in = 10
    unit_out = 20

    ! You already know total records = 13608 / 4 = 3402
    total_records = 3402

    ! Open input/output files
    open(unit=unit_in, file=infile, form='unformatted', access='sequential', action='read', status='old')
    open(unit=unit_out, file=outfile, status='replace', action='write')

    print *, 'Reading TRACK binary beam file...'
    nread = 0
    do
        read(unit_in, iostat=ios) record
        if (ios /= 0) exit

        do j = 1, nperrec
            write(*,'(6ES15.6)') (record(i,j), i=1,ncol)
            write(unit_out,'(6ES15.6)') (record(i,j), i=1,ncol)
            nread = nread + 1
        end do

        ! Show progress every 100 records
        if (mod(nread, 400) == 0) then
            percent = 100.0 * nread / (total_records * nperrec)
            write(*,'(A,F6.2,A)') 'Progress: ', percent, ' %'
        end if
    end do

    close(unit_in)
    close(unit_out)

    print *, 'Done. Total particles read:', nread
end program read_track_binary_progress

