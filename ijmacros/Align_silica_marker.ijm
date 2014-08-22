x=0; y=0;
centx=0; centy=0;

macro "Align slica marker" {
  setSlice(1);
  setTool("oval");
  for(i=1; i<=nSlices; i++) {
    waitForUser;
    wait(100);
    getSelectionBounds(x, y, width, height);
    centx = x + width/2;
    centy = y + height/2;
    //print(x+","+y+","+width+","+height);
    print(i+","+centx+","+centy);
    wait(100);
    run("Next Slice [>]");
  }
}
