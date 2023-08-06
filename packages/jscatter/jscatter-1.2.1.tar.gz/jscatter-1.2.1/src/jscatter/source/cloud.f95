!    -*- f90 -*-
! -*- coding: utf-8 -*-
! written by Ralf Biehl at the Forschungszentrum Juelich ,
! Juelich Center for Neutron Science 1 and Institute of Complex Systems 1
!    jscatter is a program to read, analyse and plot data
!    Copyright (C) 2018  Ralf Biehl
!
!    This program is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    This program is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with this program.  If not, see <http://www.gnu.org/licenses/>.
!

! f2py -c fscatter.f95 -m fscatter


module cloud
    use typesandconstants
    use utils
    !$ use omp_lib
    implicit none

contains

    function ffx(qx,r,fa,rms) result(Sq)
        ! calculates  scattering intensity I=F*conjg(F)
        ! in direction point
        ! adds rms random displacements to positions r

        ! point on unit sphere 3 x 1, scattering amplitude, positions , rms
        real(dp), intent(in) :: qx(3), fa, r(:,:), rms
        ! scattering  formfactor Sq
        real(dp)             :: Sq, rr(size(r,1),3)

        ! local variables
        complex(dp) :: iqr(size(r,1)), Fq

        if (rms>0) then
            rr=r+random_gauss(size(r,1),3)*rms
            iqr= j1 * matmul(rr,qx)
        else
            iqr= j1 * matmul( r,qx)
        end if

        Fq= sum( fa* exp(iqr) )
        Sq=REALPART(Fq*conjg( Fq ) )

    end function ffx

    function ffq(point,r,q,blength,iff,formfactor,rms,ffpolydispersity) result(res)
        ! calculates  scattering amplitude F and scattering intensity I=F*conjg(F)
        ! in direction point
        ! scales formfactor for polydispersity and adds rms random displacements to positions r

        ! point point on unit sphere 3 x 1
        real(dp), intent(in) :: point(:)
        ! wavevector scalar
        real(8), intent(in) :: q
        ! positions N x 3, scattering length xN
        real(dp), intent(in) :: r(:,:) , blength(:)
        ! indices formfactor
        integer, intent(in)     :: iff(:)
        ! formfactor ixN
        real(dp), intent(in) :: formfactor(:,:)
        ! root mean square displacements, polydispersity sigma
        real(dp), intent(in) :: rms, ffpolydispersity
        ! return value with q, formfactor F*f.conjg, scattering amplitude F
        real(dp),dimension(3) :: res

        ! local variables
        real(dp)    :: sizerms(size(r,1)), volrmsfactor(size(r,1)), fa(size(r,1)), fai(size(formfactor,2)-1)
        real(dp)    :: qx(3), rg(size(r,1),3), rg1(size(r,1),1) !, rr(size(r,1),3)
        complex(dp) :: iqr(size(r,1))
        complex(dp) :: Fq
        integer     :: i

        Fq=0*j1
        iqr=0*j1
        rg1=0_dp
        qx=0_dp
        rg=0_dp
        res=0_dp
        sizerms=0_dp
        volrmsfactor=0_dp
        fa=0_dp
        fai=0_dp

        if (ffpolydispersity>0) then
            ! normal distribution of size factor
            rg1=random_gauss(size(r,1),1)
            sizerms = rg1(:,1) * ffpolydispersity + 1_dp
            ! corresponding relative volume change
            where( sizerms <= 0._dp )  sizerms=0._dp
            volrmsfactor=sizerms**3
            ! interpolate with rms
            do i =1,size(fa,1)
                fa(i) = blength(i) * volrmsfactor(i) * interp_s(sizerms(i)*q, formfactor(1,:), formfactor(iff(i)+1,:))
            end do
        else
            ! interpolate
            do i =1,size(fai)
                fai(i) = interp_s(q, formfactor(1,:), formfactor(i+1,:))
            end do
            ! distribute according to iff
            do i =1,size(fa,1)
                fa(i)=blength(i)*fai(iff(i))
            end do
        endif

        qx=q*point
        if (rms>0) then
            rg=random_gauss(size(r,1),3)*rms
            iqr= j1 * matmul(r+rg,qx)
        else
            iqr= j1 * matmul(r   ,qx)
        end if

        Fq= sum( fa* exp(iqr) )
        res(1)=q
        res(2)=REALPART(Fq*conjg( Fq ))
        res(3)=REALPART(Fq)

    end function ffq

    function sphereaverage_ffq(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError) result(sphave)
        ! sphere average as average on fibonacci lattice for ffq
        ! returns mean

        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:),rms, ffpolydispersity
        real(dp), intent(in)    :: relError
        integer, intent(in)     :: iff(:)
        real(dp)                :: sphave(3)

        if (relError >1) then
            sphave=sphereaverage_ffqfib(q,r,blength,iff,formfactor,rms,ffpolydispersity, int(relError))
        else
            sphave=sphereaverage_ffq_pseudrand(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError)
        end if
    end function sphereaverage_ffq


    function sphereaverage_ffq_pseudrand(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError) result(sphave)
        ! sphere average  by pseudo random numbers
        ! returns mean

        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:),rms, ffpolydispersity
        real(dp), intent(in)    :: relError
        integer, intent(in)     :: iff(:)
        integer                 :: i,npoints,steps
        real(dp)                :: points(40,3),qsph(40,3),sphave(3),result(3),mean(3),prevmean(3)

        steps=40
        ! initialisation
        result=0
        qsph=randompointsonsphere(steps,0,1.0_dp)
        points=rphitheta2xyz(qsph)
        npoints = steps
        do i=1,size(points,1)
            result=result+ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
        end do
        prevmean=result/npoints
        do
            qsph=randompointsonsphere(steps,npoints,1.0_dp)
            points=rphitheta2xyz(qsph)
            npoints=npoints+steps
            do i=1,size(points,1)
                result=result+ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
            end do
            mean=result/npoints
            if ((abs(mean(2)-prevmean(2))  < relError*abs(mean(2)))  .AND. &
                (abs(mean(3)-prevmean(3))  < relError*abs(mean(3)))) then
                exit
            end if
            prevmean = mean
        end do
        sphave(1)=mean(1)
        ! calc averages
        sphave(2)=mean(2)
        sphave(3)=mean(3)

    end function sphereaverage_ffq_pseudrand

    function sphereaverage_ffqfib(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError) result(sphave)
        ! sphere average as average on fibonacci lattice for ffq
        ! returns mean

        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:),rms, ffpolydispersity
        integer, intent(in)     :: relError
        integer, intent(in)     :: iff(:)
        real(dp)                :: qfib(2*relError+1,3),points(2*relError+1,3),sphave(3),results(2*relError+1,3)
        integer                 :: i

        ! create Fibonacci lattice
        qfib=fibonacciLatticePointsOnSphere(relError,1.0_dp)
        ! to cartesian coordinates
        points=rphitheta2xyz(qfib)    ! to cartesian
        results=0
        ! for all points
        do i=1,size(points,1)
            results(i,:)=ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
        end do
        sphave(1)=q
        ! calc averages
        sphave(2)=sum(results(:,2), 1)/size(results,1)
        sphave(3)=sum(results(:,3), 1)/size(results,1)

    end function sphereaverage_ffqfib

    function scattering_Debye(q,r,blength,iff,formfactor,ncpu)  result(qsq)
    ! Debye equation  definition as in _scattering

        ! scattering vector, positions
        real(dp), intent(in)    :: q(:), blength(:)
        ! formfactor ixN
        real(dp), intent(in)    :: formfactor(:,:),r(:,:)
        ! number of cores (negative = not used cores), indices formfactor
        integer, intent(in)     :: ncpu,iff(:)
        integer                 :: k
        ! return value with q, Sq
        real(dp)                :: qsq(2,size(q,1))
        ! num of threads
        integer                 :: num_threads

        num_threads=omp_get_num_procs()
        if (ncpu<0) then
            num_threads=max(num_threads+ncpu,1)
        else if (ncpu>0) then
            num_threads=min(ncpu,num_threads)
        end if
        call omp_set_num_threads(num_threads)

        !$omp parallel do
        do k = 1,size(q,1)
            qsq(:,k)=scattering_Debye_q(q(k),r,blength,iff,formfactor)
        end do
        !$omp end parallel do

    end function scattering_Debye

    function scattering_Debye_q(q,r,blength,iff,formfactor)  result(qsq)
    ! Debye equation  for one q

        ! scattering vector, blength,formfactor ixN, positions
        real(dp), intent(in)    :: q, blength(:),formfactor(:,:),r(:,:)
        ! indices formfactor
        integer, intent(in)     :: iff(:)
        integer                 :: i,j,k
        ! return value with q, Sq
        real(dp)                :: qsq(2),qrij,sq,fa(size(formfactor,2)-1)

        qrij=0
        qsq(1)=q
        qsq(2)=0
        sq=0
        if (q==0) then
            qsq(2)=sum(blength)**2
        else
            do k =1,size(formfactor,2)-1
                fa(k) = interp_s(q, formfactor(1,:), formfactor(k+1,:))
            end do
            do i =1,size(r,1)
                do j=i+1,size(r,1)
                    qrij=q*sqrt(sum((r(i,:)-r(j,:))**2))
                    sq= sq + 2*blength(i)*fa(iff(i))*blength(j)*fa(iff(j))*sin(qrij)/qrij
                end do
                sq= sq + blength(i)**2 * fa(iff(i))**2
            end do
            qsq(2)=sq
        end if
    end function scattering_Debye_q


end module cloud
