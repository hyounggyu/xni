
<<Phantom3D`

regions = Table[Phantom3DTransformedRegion[{RotationTransform[th, {0, 0, 1}]}], {th, 0, Pi, Pi/180}];
Do[Print[i];
 data = Phantom3DRegionToImage3D[regions[[i]], 400]; 
 im = ImageAdd@Image3DSlices[data, All, 3]; 
 Export[FileNameJoin[{Environment["PWD"], "im"<>ToString@i<>".h5"}], ImageData@im];
 Print@MaxMemoryUsed[], {i, Length@regions}]
