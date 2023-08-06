!    -*- f95 -*-
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


module utils
    use typesandconstants
    use pseudorandom
    !$ use omp_lib
    implicit none

contains

function random_gauss(dim1,dim2) result(rg)
    ! Gaussian random number with center 0 and 1-sigma =1 with shape of (dim1,dim2)
    ! uses Box-Muller transform

    integer, intent(in) :: dim1,dim2
    real(dp), dimension(dim1,dim2) :: r, rg
    integer(dp) :: i
    r=0
    rg=0
    CALL RANDOM_NUMBER(r)
    do i=1,dim1-1,2
        rg(i,:)   = SQRT(-2_dp*LOG(r(i,:))) * COS(2_dp*pi_dp*r(i+1,:))
        rg(i+1,:) = SQRT(-2_dp*LOG(r(i,:))) * SIN(2_dp*pi_dp*r(i+1,:))
    end do
end function random_gauss

function interp(x,y,fy)
    ! linear interpolation of sorted array
    ! if x is out of range the upper or lower boundary value is returned

    real(dp),           intent(in)   :: x(:),y(:),fy(:)
    real(dp), dimension(size(x))    :: interp
    integer                          :: i,j,imax ,jmax

    imax=size(x)
    jmax=size(y)
    do i =1,imax
        if  (x(i)<= y(1)) then
            interp(i)=fy(1)
        else if  (x(i)>=y(jmax)) then
            interp(i)=fy(jmax)
        else
            do j=1, jmax
                if  ( y(j)<=x(i) .and. x(i)<y(j+1) )    exit
            end do
            interp(i)=interp1d_single(y(j),fy(j),y(j+1),fy(j+1),x(i))
        end if
    end do
end function interp

function interp_s(x,y,fy) result(ip2)
    ! single value linear interpolation of sorted array
    ! if x is out of range the upper or lower boundary value is returned

    real(dp),           intent(in)   :: x,y(:),fy(:)
    real(dp)                         :: res(1),ip2

    res=interp([x],y,fy)
    ip2=res(1)

end function interp_s


function interp1d_single(x1,y1,x2,y2,xval)
    ! linear interpolation
    ! xval outside interval are linear extrapolated

    real(dp),intent(in) :: x1,y1,x2,y2,xval
    real(dp) :: frac, interp1d_single
    frac = ( xval - x1 ) / ( x2 - x1 )
    interp1d_single = y1 + frac * ( y2 - y1 )
end function interp1d_single

function fibonaccilatticepointsonsphere(NN, r) result(lattice)
    ! create a Fibonacci lattice with NN*2+1 points on sphere with radius r
    ! returns spherical coordinates r,theta, phi

    integer,  intent(in)                :: NN
    real(dp), intent(in)                :: r

    real(dp), dimension(2*NN+1)         :: n
    integer                             :: i
    real(dp),dimension(2*NN+1,3)        :: lattice

    do i = 1,2*NN+1
        n(i)=(i-NN-1_dp)
    end do

    lattice(:,1)= r
    lattice(:,2)= modulo((2*pi_dp * n / golden_dp) + pi_dp,  2*pi_dp) - pi_dp
    lattice(:,3)= asin(2_dp*n / (2 * NN + 1.)) + pi_dp / 2_dp

end function fibonaccilatticepointsonsphere

function randompointsonsphere(NN, skip, r) result(lattice)
    ! create pseudo random points on sphere with radius r
    ! returns spherical coordinates r,theta, phi
    ! skip is number of points skipped in halton sequence

    integer,  intent(in)            :: NN,skip
    real(dp), intent(in)            :: r

    real(dp), dimension(2,NN)       :: hs
    real(dp), dimension(NN,3)       :: lattice

    hs=halton_sequence(skip,skip+NN-1,2)
    lattice(:,1)= r
    lattice(:,2)= 2*pi_dp*hs(1,:)- pi_dp
    lattice(:,3)= ACOS(2*hs(2,:) - 1)

end function randompointsonsphere

function rphitheta2xyz(rpt) result(xyz)
    ! transform rpt coordinates to cartesian

    real(dp), intent(in)    :: rpt(:,:)
    real(dp),dimension(size(rpt,1),3) :: xyz

    xyz(:,1)=rpt(:,1)*cos(rpt(:,2))*sin(rpt(:,3))
    xyz(:,2)=rpt(:,1)*sin(rpt(:,2))*sin(rpt(:,3))
    xyz(:,3)=rpt(:,1)*cos(rpt(:,3))

end function rphitheta2xyz

function wofz(xy) result(wxy)
    ! The Faddeeva function for complex arguments
    ! vectorized wofz
    complex(dp), intent(in)                        :: xy(:)
    complex(dp),dimension(size(xy))                :: wxy
    integer                                        :: i
    real(dp)                                       :: cx,cy

    do i = 1,size(xy)
        cx = 0_dp
        cy = 0_dp
        call ccperrfr(dreal(xy(i)), dimag(xy(i)), cx, cy)
        wxy(i) = dcmplx(cx,cy)
    end do

end function wofz

function voigt(x, center, fwhm, lg, asym, amplitude) result(val)
    ! Voigt function for peak analysis (normalized)
    ! calc the fwhm in gauss and lorenz to get the final FWHM in the Voigt function with an accuracy of 0.0002.
    ! as given in Olivero, J. J.; R. L. Longbothum (February 1977).
    ! Empirical fits to the Voigt line width: A brief review".
    ! Journal of Quantitative Spectroscopy and Radiative Transfer. 17 (2): 233-236.
    ! doi:10.1016/0022-4073(77)90161-3

    ! x, center, fwhm, Lorenzian/gaussian fraction, symmetry factor, amplitude
    real(dp), intent(in)          :: x(:), center, fwhm, lg, asym, amplitude
    real(dp),dimension(size(x))   :: val
    real(dp)                      :: fw
    real(dp),dimension(size(x))   :: afwhm
    complex(dp),dimension(size(x)):: z,wofzz
    integer                       :: i

    fw = fwhm / (0.5346 * lg + (0.2166 * lg ** 2 + 1) ** 0.5)

    ! the sigmoidal fwhm for asymmetry
    afwhm = 2.0_dp * fw / (1.0_dp + exp(asym * (x - center)))

    ! complex z
    z =  dcmplx((x - center), lg * afwhm / 2.0_dp)
    z = z / sqrt(2.0_dp) / (afwhm / (2.0_dp * sqrt(2.0_dp * ln2)))

    val = amplitude / (afwhm / (2 * sqrt(2.0_dp * ln2))) / sqrt(2.0_dp * pi_dp)

    wofzz = wofz(z)
    do i = 1,size(x)
        val(i)=val(i) * dreal(  wofzz(i)  )
    end do

end function voigt

function sumlhklvoigt(q, qhkl, f2hkl, mhkl,lg, domainsize, asym, dim, c, n, vd, ncpu) result(Z0q)
    ! This calculates the sum over peak shapes in radial structure factor
    ! voigt peak shapes over all hkl peak indices
    real(dp), intent(in)          :: q(:), qhkl(:), f2hkl(:), mhkl(:), lg, domainsize, asym, c, n, vd
    integer, intent(in)           :: dim, ncpu
    real(dp),dimension(size(q))   :: Z0q
    integer                       :: i,num_threads

    num_threads=omp_get_num_procs()
    if (ncpu<0) then
        num_threads=max(num_threads+ncpu,1)
    else if (ncpu>0) then
        num_threads=min(ncpu,num_threads)
    end if
    call omp_set_num_threads(num_threads)

    ! sum lattice factors
    Z0q=0
    !$omp parallel do
    do i=1,size(qhkl)
        Z0q = Z0q + mhkl(i) * f2hkl(i) * voigt(q, qhkl(i), pi2_dp/domainsize, lg, asym, 1.0_dp)
    end do
    !$omp end parallel do

    ! normalisations
    Z0q = Z0q *(pi2_dp) ** (dim - 1) * c / n / vd / q ** (dim - 1)

end function sumlhklvoigt

function lhklgauss(q,center,sigma) result(lhkl)
    ! calculates intensities of normalized Gaussian peak in 3 dimensions with width sigma located at center
    ! for given 3D q values

    ! wavevectors Nx3, center and width of peak in each dimension
    real(dp), intent(in) :: q(:,:), center(3),sigma(3)
    ! center shifted q_i, result array
    real(dp)             :: qc(size(q,1)),lhkl(size(q,1))

    qc(:)=q(:,1)-center(1)
    lhkl=exp(-0.5_dp*qc**2/sigma(1)**2)/sigma(1)/sqrt(pi2_dp)
    qc(:)=q(:,2)-center(2)
    lhkl=lhkl*exp(-0.5_dp*qc**2/sigma(2)**2)/sigma(2)/sqrt(pi2_dp)
    qc(:)=q(:,3)-center(3)
    lhkl=lhkl*exp(-0.5_dp*qc**2/sigma(3)**2)/sigma(3)/sqrt(pi2_dp)

end function lhklgauss

function sumlhklgauss(q,centers,sigma,f2,ncpu) result(sumlhkl)
    ! calculates intensities of normalized Gaussian peak in 3 dimensions with width sigma located at center
    ! for given 3D q values
    ! q should be >0

    ! wavevectors Nx3, center and width of peak in each dimension, f2 multiplicity of a peak
    real(dp), intent(in) :: q(:,:), centers(:,:), sigma(3), f2(:)
    ! number of cores (negative = not used cores)
    integer, intent(in)     :: ncpu
    ! center shifted q_i, result array
    real(dp)             :: sumlhkl(size(q,1))
    integer                 :: i
    ! num of threads
    integer                 :: num_threads

    num_threads=omp_get_num_procs()
    if (ncpu<0) then
        num_threads=max(num_threads+ncpu,1)
    else if (ncpu>0) then
        num_threads=min(ncpu,num_threads)
    end if
    call omp_set_num_threads(num_threads)

    sumlhkl=0

    !$omp parallel do
    do i=1,size(centers,1)
        sumlhkl=sumlhkl+f2(i)*lhklgauss(q,centers(i,:),sigma)
    end do
    !$omp end parallel do

end function sumlhklgauss


end module utils
