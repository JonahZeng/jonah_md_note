# opencv的插值
请参看函数cvtcolor();    CV_BAYER_BG2RGB等宏flag
# 函数定义

```c
struct RGBinfo{
               BYTE B;
               BYTE G;
               BYTE R;
               };
               
```
RGBinfo**  bmpbuffer是一个静态二维数组或者动态分配内存的二维数组
```c
void CbmpView::RawInterpolation(RGBinfo** bmpbuffer,unsigned short** rawbuffer, UINT InterpolationMode,UINT rawBit,UINT rawWidth,UINT rawHeight)
{
	
	
	switch (InterpolationMode)
	{ 
	case RG:
		for (UINT i = 0; i< rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				if (i % 2 == 0 && j % 2 == 0)
				{
					bmpbuffer[i][j].R = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].B = 0;
					bmpbuffer[i][j].G = 0;
				}
				else if (i % 2 == 1 && j % 2 == 1)
				{
					bmpbuffer[i][j].B = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].R = 0;
					bmpbuffer[i][j].G = 0;
				}
				else
				{
					bmpbuffer[i][j].G = rawbuffer[i][j] >> (rawBit-8);
					bmpbuffer[i][j].R = 0;
					bmpbuffer[i][j].B = 0;
				}
			}
		}
		for (UINT i = 0; i < rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				bmpbuffer[0][0].G = (bmpbuffer[0][1].G+bmpbuffer[1][0].G)/2;//R   the frist pixel
				bmpbuffer[0][0].B = bmpbuffer[1][1].B;//R
				bmpbuffer[0][rawWidth - 1].R = bmpbuffer[0][rawWidth - 2].R;//the last pixel of frist line  G
				bmpbuffer[0][rawWidth - 1].B = bmpbuffer[1][rawWidth - 1].B;

				bmpbuffer[rawHeight - 1][0].B = bmpbuffer[rawHeight - 1][1].B;//G
				bmpbuffer[rawHeight - 1][0].R = bmpbuffer[rawHeight - 2][0].R;
				bmpbuffer[rawHeight - 1][rawWidth - 1].R = bmpbuffer[rawHeight - 2][rawWidth - 2].R;//B
				bmpbuffer[rawHeight - 1][rawWidth - 1].G = (bmpbuffer[rawHeight - 1][rawWidth - 2].G+bmpbuffer[rawHeight-2][rawWidth-1].G)/2;
				if (i == 0 && j != 0 && j != rawWidth - 1)//the frist line  RGRGRGRGRG
				{                                                        // GBGBGBGBGB
					if (j % 2 == 1)//G
					{
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
						bmpbuffer[i][j].B = bmpbuffer[i + 1][j].B;
					}
					else//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G+bmpbuffer[i+1][j].G) / 3;
						bmpbuffer[i][j].B = (bmpbuffer[i + 1][j-1].B+bmpbuffer[i+1][j+1].B)/2;
					}
				}

				if (i == rawHeight - 1 && j != 0 && j != rawWidth - 1)//the last line
				{
					if (j % 2 == 1)//B
					{
						bmpbuffer[i][j].R = (bmpbuffer[i-1][j-1].R + bmpbuffer[i-1][j+1].R) / 2;
						bmpbuffer[i][j].G = (bmpbuffer[i-1][j].G+bmpbuffer[i][j-1].G+bmpbuffer[i][j+1].G) / 3;
					}
					else//G
					{
						bmpbuffer[i][j].B = (bmpbuffer[i][j-1].B+bmpbuffer[i][j+1].B) / 2;
						bmpbuffer[i][j].R = bmpbuffer[i - 1][j].R;
					}
				}

				if (j == 0 && i != 0 && i != rawHeight - 1)//the frist row   RGRG
				{                                                        //  GBGB
					if (i % 2 == 1)//G                                       RGRG
					{                  //                                    GBGB
						bmpbuffer[i][j].B = bmpbuffer[i][j + 1].B;
						bmpbuffer[i][j].R = (bmpbuffer[i-1][j].R+bmpbuffer[i+1][j].R) / 2;
					}
					else//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j + 1].G+bmpbuffer[i-1][j].G+bmpbuffer[i+1][j].G)/3;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j+1].B + bmpbuffer[i + 1][j+1].B) / 2;
					}
				}

				if (j == rawWidth - 1 && i != 0 && i != rawHeight - 1)//the last row
				{
					if (i % 2 == 1)//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G+bmpbuffer[i-1][j].G+bmpbuffer[i+1][j].G)/3;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j-1].R + bmpbuffer[i + 1][j-1].R) / 2;
					}
					else//G
					{
						bmpbuffer[i][j].R = bmpbuffer[i][j-1].R;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
					}
				}

				if (i > 0 && i < rawHeight - 1 && j>0 && j < rawWidth - 1)//RGRGRG
				{                                                         //GBGBGB
					if (i % 2 == 0 && j % 2 == 1)//G                      //RGRGRG
					{                                                     //GBGBGB
						bmpbuffer[i][j].R = (bmpbuffer[i][j-1].R+bmpbuffer[i][j+1].R)/2;
						bmpbuffer[i][j].B = (bmpbuffer[i-1][j].B+bmpbuffer[i+1][j].B)/2;
					}
					else if (i % 2 == 1 && j % 2 == 0)//G
					{
						bmpbuffer[i][j].R = (bmpbuffer[i-1][j].R+bmpbuffer[i+1][j].R)/2;
						bmpbuffer[i][j].B = (bmpbuffer[i][j-1].B+bmpbuffer[i][j+1].B)/2;
					}
					else if (i % 2 == 1 && j % 2 == 1)//B
					{
						bmpbuffer[i][j].R = (bmpbuffer[i-1][j-1].R+bmpbuffer[i-1][j+1].R+bmpbuffer[i+1][j-1].R+bmpbuffer[i+1][j+1].R)/4;
						bmpbuffer[i][j].G = (bmpbuffer[i-1][j].G+bmpbuffer[i+1][j].G+bmpbuffer[i][j-1].G+bmpbuffer[i][j+1].G)/4;
					}
					else//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i-1][j].G + bmpbuffer[i+1][j].G+bmpbuffer[i][j-1].G+bmpbuffer[i][j+1].G) / 4;
						bmpbuffer[i][j].B = (bmpbuffer[i-1][j-1].B + bmpbuffer[i-1][j+1].B+bmpbuffer[i+1][j-1].B+bmpbuffer[i+1][j+1].B) / 4;
					}
				}
			}
		}
		break;
	case GR:
		for (UINT i = 0; i< rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				if (i % 2 == 0 && j % 2 == 1)
				{
					bmpbuffer[i][j].R = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].B = 0;
					bmpbuffer[i][j].G = 0;
				}
				else if (i % 2 == 1 && j % 2 == 0)
				{
					bmpbuffer[i][j].B = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].R = 0;
					bmpbuffer[i][j].G = 0;
				}
				else
				{
					bmpbuffer[i][j].G = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].B = 0;
					bmpbuffer[i][j].R = 0;
				}
				
			}//for(UINT j=0.....)
		}//for(UINT i=0.....)

		for (UINT i = 0; i < rawHeight;i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				bmpbuffer[0][0].R = bmpbuffer[0][1].R;
				bmpbuffer[0][0].B = bmpbuffer[1][0].B;
				bmpbuffer[0][rawWidth - 1].G = (bmpbuffer[0][rawWidth - 2].G + bmpbuffer[1][rawWidth - 1].G) / 2;
				bmpbuffer[0][rawWidth - 1].B = bmpbuffer[1][rawWidth - 2].B;

				bmpbuffer[rawHeight - 1][0].G = (bmpbuffer[rawHeight - 2][0].G + bmpbuffer[rawHeight - 1][1].G) / 2;
				bmpbuffer[rawHeight - 1][0].R = bmpbuffer[rawHeight - 2][1].R;
				bmpbuffer[rawHeight - 1][rawWidth - 1].R = bmpbuffer[rawHeight - 2][rawWidth - 1].R;
				bmpbuffer[rawHeight - 1][rawWidth - 1].B = bmpbuffer[rawHeight - 1][rawWidth - 2].B;
				if (i == 0 && j != 0 && j != rawWidth - 1)//the frist line
				{
					if (j % 2 == 1)//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].B = (bmpbuffer[i + 1][j - 1].B + bmpbuffer[i + 1][j + 1].B) / 2;
					}
					else//G
					{
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
						bmpbuffer[i][j].B = bmpbuffer[i + 1][j].B;
					}
				}

				if (i == rawHeight - 1 && j != 0 && j != rawWidth - 1)//the last line
				{
					if (j % 2 == 1)//G
					{
						bmpbuffer[i][j].R = bmpbuffer[i - 1][j].R;
						bmpbuffer[i][j].B = (bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 2;
					}
					else//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i - 1][j].G + bmpbuffer[i][j + 1].G) / 3;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j - 1].R + bmpbuffer[i - 1][j + 1].R) / 2;
					}
				}

				if (j == 0 && i != 0 && i != rawHeight - 1)//the frist row
				{
					if (i % 2 == 1)//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j + 1].G) / 3;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j + 1].R + bmpbuffer[i + 1][j + 1].R) / 2;
					}
					else//G
					{
						bmpbuffer[i][j].R = bmpbuffer[i][j + 1].R;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
					}
				}

				if (j == rawWidth - 1 && i != 0 && i != rawHeight - 1)//the last row
				{
					if (i % 2 == 1)//G
					{
						bmpbuffer[i][j].B = bmpbuffer[i][j - 1].B;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j].R + bmpbuffer[i + 1][j].R) / 2;
					}
					else//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j - 1].B + bmpbuffer[i + 1][j - 1].B) / 2;
					}
				}

				if (i > 0 && i < rawHeight - 1 && j>0 && j < rawWidth - 1)
				{
					if (i % 2 == 0 && j % 2 == 1)//R
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j - 1].B + bmpbuffer[i - 1][j + 1].B + bmpbuffer[i + 1][j - 1].B + bmpbuffer[i + 1][j + 1].B) / 4;
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G) / 4;
					}
					else if (i % 2 == 1 && j % 2 == 0)//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G) / 4;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j - 1].R + bmpbuffer[i - 1][j + 1].R + bmpbuffer[i + 1][j - 1].R + bmpbuffer[i + 1][j + 1].R) / 4;
					}
					else if (i%2==1&&j%2==1)
					{
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j].R + bmpbuffer[i + 1][j].R) / 2;
						bmpbuffer[i][j].B = (bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 2;
					}
					else
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
					}
				}
			}
		}
		break;
	case BG:
		for (UINT i = 0; i< rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				if (i % 2 == 0 && j % 2 == 0)
				{
					bmpbuffer[i][j].B = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].R = 0;
					bmpbuffer[i][j].G = 0;
				}
				else if (i % 2 == 1 && j % 2 == 1)
				{
					bmpbuffer[i][j].R = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].B = 0;
					bmpbuffer[i][j].G = 0;
				}
				else
				{
					bmpbuffer[i][j].G = rawbuffer[i][j] >> (rawBit - 8);
					bmpbuffer[i][j].R = 0;
					bmpbuffer[i][j].B = 0;
				}
			}
		}
		/*
		BGBGBGBG
		GRGRGRGR
		BGBGBGBG
		GRGRGRGR
		*/

		for (UINT i = 0; i < rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				bmpbuffer[0][0].G = (bmpbuffer[0][1].G + bmpbuffer[1][0].G) / 2;//B   the frist pixel
				bmpbuffer[0][0].R = bmpbuffer[1][1].R;
				bmpbuffer[0][rawWidth - 1].B = bmpbuffer[0][rawWidth - 2].B;//the last pixel of frist line  G
				bmpbuffer[0][rawWidth - 1].R = bmpbuffer[1][rawWidth - 1].R;

				bmpbuffer[rawHeight - 1][0].R = bmpbuffer[rawHeight - 1][1].R;//G
				bmpbuffer[rawHeight - 1][0].B = bmpbuffer[rawHeight - 2][0].B;
				bmpbuffer[rawHeight - 1][rawWidth - 1].B = bmpbuffer[rawHeight - 2][rawWidth - 2].B;
				bmpbuffer[rawHeight - 1][rawWidth - 1].G = (bmpbuffer[rawHeight - 1][rawWidth - 2].G + bmpbuffer[rawHeight - 2][rawWidth - 1].G) / 2;
				if (i == 0 && j != 0 && j != rawWidth - 1)//the frist line  
				{                                                    
					if (j % 2 == 1)//G
					{
						bmpbuffer[i][j].B = (bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 2;
						bmpbuffer[i][j].R = bmpbuffer[i + 1][j].R;
					}
					else//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].R = (bmpbuffer[i + 1][j - 1].R + bmpbuffer[i + 1][j + 1].R) / 2;
					}
				}

				if (i == rawHeight - 1 && j != 0 && j != rawWidth - 1)//the last line
				{
					if (j % 2 == 1)//R
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j - 1].B + bmpbuffer[i - 1][j + 1].B) / 2;
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G) / 3;
					}
					else//G
					{
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
						bmpbuffer[i][j].B = bmpbuffer[i - 1][j].B;
					}
				}

				if (j == 0 && i != 0 && i != rawHeight - 1)//the frist row   BGBG
				{                                                        //  GRGR
					if (i % 2 == 1)//G                                       BGBG
					{                  //                                    GRGR
						bmpbuffer[i][j].R = bmpbuffer[i][j + 1].R;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
					}
					else//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j + 1].G + bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j + 1].R + bmpbuffer[i + 1][j + 1].R) / 2;
					}
				}

				if (j == rawWidth - 1 && i != 0 && i != rawHeight - 1)//the last row
				{
					if (i % 2 == 1)//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j - 1].B + bmpbuffer[i + 1][j - 1].B) / 2;
					}
					else//G
					{
						bmpbuffer[i][j].B = bmpbuffer[i][j - 1].B;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j].R + bmpbuffer[i + 1][j].R) / 2;
					}
				}

				if (i > 0 && i < rawHeight - 1 && j>0 && j < rawWidth - 1)//BGBGBGBG
				{                                                         //GRGRGRGR
					if (i % 2 == 0 && j % 2 == 1)//G                      //BGBGBGBG
					{                                                     //GRGRGRGR
						bmpbuffer[i][j].B = (bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 2;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j].R + bmpbuffer[i + 1][j].R) / 2;
					}
					else if (i % 2 == 1 && j % 2 == 0)//G
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
					}
					else if (i % 2 == 1 && j % 2 == 1)//R
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j - 1].B + bmpbuffer[i - 1][j + 1].B + bmpbuffer[i + 1][j - 1].B + bmpbuffer[i + 1][j + 1].B) / 4;
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G) / 4;
					}
					else//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G) / 4;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j - 1].R + bmpbuffer[i - 1][j + 1].R + bmpbuffer[i + 1][j - 1].R + bmpbuffer[i + 1][j + 1].R) / 4;
					}
				}
			}
		}
		break;
	case GB:
		for (UINT i = 0; i< rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				if (i % 2 == 0 && j % 2 == 1)
				{
					bmpbuffer[i][j].B = rawbuffer[i][j] >> (rawBit - 8);
				}
				else if (i % 2 == 1 && j % 2 == 0)
				{
					bmpbuffer[i][j].R = rawbuffer[i][j] >> (rawBit - 8);
				}
				else
				{
					bmpbuffer[i][j].G = rawbuffer[i][j] >> (rawBit - 8);
				}
			}
		}
		/*
		GBGBGBGB
		RGRGRGRG
		GBGBGBGB
		RGRGRGRG
		 */
		for (UINT i = 0; i < rawHeight; i++)
		{
			for (UINT j = 0; j < rawWidth; j++)
			{
				bmpbuffer[0][0].B = bmpbuffer[0][1].B;
				bmpbuffer[0][0].R = bmpbuffer[1][0].R;
				bmpbuffer[0][rawWidth - 1].G = (bmpbuffer[0][rawWidth - 2].G + bmpbuffer[1][rawWidth - 1].G) / 2;
				bmpbuffer[0][rawWidth - 1].R = bmpbuffer[1][rawWidth - 2].R;

				bmpbuffer[rawHeight - 1][0].G = (bmpbuffer[rawHeight - 2][0].G + bmpbuffer[rawHeight - 1][1].G) / 2;
				bmpbuffer[rawHeight - 1][0].B = bmpbuffer[rawHeight - 2][1].B;
				bmpbuffer[rawHeight - 1][rawWidth - 1].B = bmpbuffer[rawHeight - 2][rawWidth - 1].B;
				bmpbuffer[rawHeight - 1][rawWidth - 1].R = bmpbuffer[rawHeight - 1][rawWidth - 2].R;
				if (i == 0 && j != 0 && j != rawWidth - 1)//the frist line
				{
					if (j % 2 == 1)//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].R = (bmpbuffer[i + 1][j - 1].R + bmpbuffer[i + 1][j + 1].R) / 2;
					}
					else//G
					{
						bmpbuffer[i][j].B = (bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 2;
						bmpbuffer[i][j].R = bmpbuffer[i + 1][j].R;
					}
				}

				if (i == rawHeight - 1 && j != 0 && j != rawWidth - 1)//the last line
				{
					if (j % 2 == 1)//G
					{
						bmpbuffer[i][j].B = bmpbuffer[i - 1][j].B;
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
					}
					else//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i][j - 1].G + bmpbuffer[i - 1][j].G + bmpbuffer[i][j + 1].G) / 3;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j - 1].B + bmpbuffer[i - 1][j + 1].B) / 2;
					}
				}
				
				if (j == 0 && i != 0 && i != rawHeight - 1)//the frist row
				{
					if (i % 2 == 1)//R
					{
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j + 1].G) / 3;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j + 1].B + bmpbuffer[i + 1][j + 1].B) / 2;
					}
					else//G
					{
						bmpbuffer[i][j].B = bmpbuffer[i][j + 1].B;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j].R + bmpbuffer[i + 1][j].R) / 2;
					}
				}

				if (j == rawWidth - 1 && i != 0 && i != rawHeight - 1)//the last row
				{
					if (i % 2 == 1)//G
					{
						bmpbuffer[i][j].R = bmpbuffer[i][j - 1].R;
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
					}
					else//B
					{
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i + 1][j].G) / 3;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j - 1].R + bmpbuffer[i + 1][j - 1].R) / 2;
					}
				}
				/*
				GBGBGBGB
				RGRGRGRG
				GBGBGBGB
				RGRGRGRG
				*/
				if (i > 0 && i < rawHeight - 1 && j>0 && j < rawWidth - 1)
				{
					if (i % 2 == 0 && j % 2 == 1)//B
					{
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j - 1].R + bmpbuffer[i - 1][j + 1].R + bmpbuffer[i + 1][j - 1].R + bmpbuffer[i + 1][j + 1].R) / 4;
						bmpbuffer[i][j].G = (bmpbuffer[i - 1][j].G + bmpbuffer[i + 1][j].G + bmpbuffer[i][j - 1].G + bmpbuffer[i][j + 1].G) / 4;
					}
					else if (i % 2 == 1 && j % 2 == 0)//R
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B + bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 4;
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j - 1].R + bmpbuffer[i - 1][j + 1].R + bmpbuffer[i + 1][j - 1].R + bmpbuffer[i + 1][j + 1].R) / 4;
					}
					else if (i % 2 == 1 && j % 2 == 1)
					{
						bmpbuffer[i][j].B = (bmpbuffer[i - 1][j].B + bmpbuffer[i + 1][j].B) / 2;
						bmpbuffer[i][j].R = (bmpbuffer[i][j - 1].R + bmpbuffer[i][j + 1].R) / 2;
					}
					else
					{
						bmpbuffer[i][j].R = (bmpbuffer[i - 1][j].R + bmpbuffer[i + 1][j].R) / 2;
						bmpbuffer[i][j].B = (bmpbuffer[i][j - 1].B + bmpbuffer[i][j + 1].B) / 2;
					}
				}
			}
		}
		break;
	}
}
```