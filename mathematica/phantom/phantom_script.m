<<Phantom3D`

regions = Table[Phantom3DTransformedRegion[{RotationTransform[th, {0, 0, 1}]}], {th, 0, Pi, Pi/180}];
im = ImageAdd@Image3DSlices[Phantom3DRegionToImage3D[#, 400], All, 3]& /@ regions 
Export[FileNameJoin[{Environment["PWD"], "im.h5"}], ImageData/@im];
