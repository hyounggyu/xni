(* ::Package:: *)

(*:Mathematica Version: 10.0 *)

(*:Package Version: 0.01*)

(*:License: GPL*)

(*:Name: Phantom3D` *)

(*:Author: Hyounggyu Kim (khg@gist.ac.kr) *)

BeginPackage["Phantom3D`"]

Phantom3D::usage = "Phantom Head"

Phantom3DRegion::usage = "Make Region"

Phantom3DRegionToData::usage = "Region to Image"

Begin["`Private`"]

head={
	(* Coordinates of the center, Axis lengths(a,b,c), Euler angle phi(radian)*)
	{{0,0,0},{0.69,0.92,0.9},0},
	{{0,0,0},{0.6624,0.874,0.88},0},
	{{-0.22,0,-0.25},{0.41,0.16,0.21},(3 Pi)/5},
	{{0.22,0,-0.25},{0.31,0.11,0.22},(2 Pi)/5},
	{{0,0.35,-0.25},{0.21,0.25,0.5},0},
	{{0,0.1,-0.25},{0.046,0.046,0.046},0},
	{{-0.08,-0.65,-0.25},{0.046,0.023,0.02},0},
	{{0.06,-0.65,-0.25},{0.046,0.023,0.02},0},
	{{0.06,-0.105,0.625},{0.056,0.04,0.1},Pi/2},
	{{0,0.1,0.625},{0.056,0.056,0.1},Pi/2}
};

(* Gray levels *)
rho={2.0,-0.8,-0.2,-0.2,0.2,0.2,0.1,0.1,0.2,-0.2};

Phantom3D[]:=head/.{center_,axislengths_,phi_}->Ellipsoid[center,RotationMatrix[Pi-phi,{0,0,1}].DiagonalMatrix@(axislengths^2).Transpose@RotationMatrix[Pi-phi,{0,0,1}]]

Phantom3DRegion[args_List]:=Fold[TransformedRegion,#,args]&/@(Phantom3D[])

Phantom3DRegionToData[region_,points_]:=Module[{mf},
	mf=RegionMember/@(region);
	Plus@@(rho Boole@Through@mf@points)
]

End[]

EndPackage[]






