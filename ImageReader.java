import java.awt.image.BufferedImage;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import javax.imageio.ImageIO;


/**
 * @author Daniel Nussenbaum
 *
 */
public class ImageReader {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		System.out.println("Starting to read images");
		ImageReader ir = new ImageReader();
		ir.writeReps();
		System.out.println("Representations have been written, please execute \"python danielnussenbaum_Project_3.py\" in the terminal");
	}

	boolean ddd = false;
	
	public void writeReps()
	{
		for(int i = 1; i <= 8; i++)
		{
			File f;
			f=new File("Representations/3-"+i+".txt");
			if(!f.exists()){
				try {
					f.createNewFile();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			
			BufferedWriter bw = null;
	        try {
				bw = new BufferedWriter(new FileWriter("Representations/3-"+i+".txt"));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        
	        try {
				bw.write("<data>");
				bw.newLine();
				bw.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			
		}
		File f = new File("Frames");
		String[] fileList = f.list();
//		syso(fileList.length);
//		syso(java.util.Arrays.toString(fileList[0].split("\\.")));
		for(int i = 0; i < fileList.length; i++)
		{
			String[] temp = fileList[i].split("\\.");
//			output.add(temp[0].substring(0, 3));
//			output.add(temp[0].substring(3));
//			if(temp[0].substring(0, 3).compareTo("3-4")==0)
//			System.out.println(temp[0].substring(3));
			readImage("Frames/"+fileList[i],temp[0].substring(0, 3),temp[0].substring(3));
//			output.add();
		}


		for(int i = 1; i <= 8; i++)
		{
			BufferedWriter bw = null;
	        try {
				bw = new BufferedWriter(new FileWriter("Representations/3-"+i+".txt", true));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        
	        try {
				bw.write("</data>");
				bw.newLine();
				bw.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			
		}
	}
	
	public void readImage(String file, String text, String frame)
	{
		ArrayList<String> output = new ArrayList<String>();
		BufferedWriter bw = null;
        try {
			bw = new BufferedWriter(new FileWriter("Representations/"+text+".txt", true));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        // System.out.println("file: " + file);
        // System.out.println("text: " + text);
        // System.out.println("frame: " + frame);

        boolean solFrame = false;
        if(frame.length() >= 3 && frame.substring(0,3).equalsIgnoreCase("Ans")){
        	solFrame = true;
        }

        try {
        	if(solFrame)
        		bw.write("<sframe index=\"" +frame + "\">");
        	else
				bw.write("<frame index=\"" +frame + "\">");
			bw.newLine();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		BufferedImage image = null;
		try {
			image = ImageIO.read(new File(file));
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		int width = image.getWidth();
		int height = image .getHeight();
		int[][] pixels = new int[width][height];
		int startx = 0, starty = 0;
		for( int i = 0; i < height; i++)
		{
//			output.add();
		    for( int j = 0; j < width; j++)
		    {
		        pixels[j][i] = image.getRGB(j,i);
//		        if(pixels[j][i]==-1)
//		        	System.out.print("-1      ");
//		        else
//		        	System.out.print(pixels[j][i]);
		    }
		}
		
		// output.add("NumObjs : ");
		int numObjs = 1;
		for( int i = 0; i < height; i++)
		{
		    for( int j = 0; j < width; j++)
		    {
		    	if(pixels[j][i]!=-1)
		    	{
		    		startx = j;
		    		starty = i;
		    		if(vLine(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    		if(hLine(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    		if(pacman(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    		if(square(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    		if(square45(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    		if(plus(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println("circle " + numObjs);
		    		if(circle(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    		if(triangle(pixels, startx, starty, output, numObjs))
		    			numObjs++;
//		    		System.out.println(numObjs);
		    	}
		    }
		}
//		System.out.println(output.size());
		numObjs--;
		try {
			bw.write(output.get(0));//+numObjs);
			bw.newLine();
			for(int i = 1; i < output.size();i++)
			{
				bw.write(output.get(i));
				bw.newLine();
			}
			// bw.write("End " +frame + " :");
			if(solFrame)
				bw.write("</sframe>");
			else
				bw.write("</frame>");
			bw.newLine();
			bw.close();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}
	
	public boolean vLine(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		int size;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = (x+x+i)/2;
		i=0;
		if(midx < 4)
			return false;
		if(midx+4 >=79)
			return false;
		while(data[midx][y+i]!=-1 && data[midx-4][y+i]!=-1 && data[midx+4][y+i]!=-1)
		{
			i++;
			if(y+i>=79)
				return false;
		}
		int temp = i;
		int fill = 0;
		while(data[midx][y+i]!=-1)
		{
			if(data[midx-4][y+i]==-1 && data[midx+4][y+i]==-1)
			{
//				System.out.println("hi");
//				data[midx][y+i] = -1;
//				data[midx+1][y+i] = -1;
//				data[midx+2][y+i] = -1;
//				data[midx+3][y+i] = -1;
//				data[midx-1][y+i] = -1;
//				data[midx-2][y+i] = -1;
//				data[midx-3][y+i] = -1;
			}
			else
			{
				fill++;
			}
			i++;
		}
		int shapey = i-temp-fill;
		int midy = (y+y+i)/2;
		size = shapey/8;
		if(size > 2)
		{
			// output.add("Start Obj"+numObjs+" :");
			output.add("<figure index=\""+numObjs+"\">");
			output.add("<x> " + midx/8 + "</x>");
			output.add("<y>"+midy/8 +"</y>");
			output.add("<rotation> 0</rotation>");
			output.add("<size>"+size+"</size>");
			output.add("<shape>Line</shape>");
			output.add("<filled>0</filled>");
			output.add("<reflected>0</reflected>");
			output.add("</figure>");
			
			while(data[midx][y+temp]!=-1)
			{
				if(data[midx-4][y+temp]==-1 && data[midx+4][y+temp]==-1)
				{
					data[midx][y+temp] = -1;
					data[midx+1][y+temp] = -1;
					data[midx+2][y+temp] = -1;
					data[midx+3][y+temp] = -1;
					data[midx-1][y+temp] = -1;
					data[midx-2][y+temp] = -1;
					data[midx-3][y+temp] = -1;
				}
				temp++;
			}
//			for(int n = 0; n < data.length; n++)
//			{
//				System.out.println();
//				for(int m = 0; m < data.length; m++)
//				{
//					if(data[n][m]==-1)
//						System.out.print("-1       ");
//					else
//						System.out.print(data[n][m]);
//				}
//			}
//			System.out.println("WTF");
			return true;
	
		}
		
		return false;
	}
	
	public boolean hLine(int[][] data, int x, int y, ArrayList<String> output, int numObjs )
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		int midy = y+3;
		if(midy-4<0)
			return false;
		boolean lineOnly = true;
		while(data[x+i][midy]!=-1)
		{
			i++;
			if(data[x+i][midy-4]!=-1 || data[x+i][midy+4]!=-1)
				lineOnly = false;
		}
		int size = (i-5)/8;
		if(size>2 && lineOnly)
		{
			i = 0;
			while(data[x+i][midy]!=-1)
			{
				data[x+i][midy] = -1;
				data[x+i][midy+1] = -1;
				data[x+i][midy+2] = -1;
				data[x+i][midy+3] = -1;
				data[x+i][midy-1] = -1;
				data[x+i][midy-2] = -1;
				data[x+i][midy-3] = -1;
				i++;
			}
			int midx = (x+x+i)/2;
						
			// output.add("Start Obj"+numObjs+" :");
			// output.add("X : " + midx/8);
			// output.add("Y : "+midy/8);
			// output.add("Rotation : 180");
			// output.add("Size : "+size);
			// output.add("Shape : Line");
			// output.add("Filled : 0");
			// output.add("Reflected : 0");
			// output.add("End Obj"+numObjs+" :");


			output.add("<figure index=\""+numObjs+"\">");
			output.add("<x> " + midx/8 + "</x>");
			output.add("<y>"+midy/8 +"</y>");
			output.add("<rotation> 180</rotation>");
			output.add("<size>"+size+"</size>");
			output.add("<shape>Line</shape>");
			output.add("<filled>0</filled>");
			output.add("<reflected>0</reflected>");
			output.add("</figure>");
			
			return true;
		}
		
		i = 0;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = (x+x+i)/2;
		i=0;
		while(data[midx][y+i]!=-1)
		{
			i++;
		}
		if(i<12)
		{
			while(data[midx][y+i]==-1 && y+i<data.length-1)
			{
				i++;
			}
			y = y+i;
			i=0;
			while(data[midx+i][y]!=-1 && midx+i>0)
			{
				i--;
			}
			x = midx+i+1;
			
			
			i=0;
			midy = y+3;
			if(midy<4 || midy > data.length-5)
				return false;
			while(data[x+i][midy]!=-1 && data[x+i][midy-4]!=-1 && data[x+i][midy+4]!=-1)
			{
				i++;
			}
			if(i>0)
			{
				int temp = i;
				while(data[x+i][midy]!=-1)
				{
					if(data[x+i][midy-4]==-1 && data[x+i][midy+4]==-1)
					{
						data[x+i][midy] = -1;
						data[x+i][midy+1] = -1;
						data[x+i][midy+2] = -1;
						data[x+i][midy+3] = -1;
						data[x+i][midy-1] = -1;
						data[x+i][midy-2] = -1;
						data[x+i][midy-3] = -1;
					}
					i++;
				}
				int shapex = i-temp-5;
				midy = (y+y+i)/2;
				size = shapex/8;
				if(size > 2)
				{
					// output.add("Start Obj"+numObjs+" :");
					// output.add("X : " + midx/8);
					// output.add("Y : "+midy/8);
					// output.add("Rotation : 180");
					// output.add("Size : "+size);
					// output.add("Shape : Line");
					// output.add("Filled : 0");
					// output.add("Reflected : 0");
					// output.add("End Obj"+numObjs+" :");


					output.add("<figure index=\""+numObjs+"\">");
					output.add("<x> " + midx/8 + "</x>");
					output.add("<y>"+midy/8 +"</y>");
					output.add("<rotation> 180</rotation>");
					output.add("<size>"+size+"</size>");
					output.add("<shape>Line</shape>");
					output.add("<filled>0</filled>");
					output.add("<reflected>0</reflected>");
					output.add("</figure>");

					return true;		
				}
			}
		}
		return false;
	}
	
	public boolean square(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int j = 0;
		while(data[x][y+j]!=-1)
		{
			j++;
		}
		int size = i/8;
		if(i==j && size>2)
		{
			int midx = (x+x+i)/2;
			int midy = (y+y+i)/2;
			
			// output.add("Start Obj"+numObjs+" :");
			// output.add("X : " + midx/8);
			// output.add("Y : "+midy/8);
			// output.add("Rotation : 0");
			// output.add("Size : "+size);
			// output.add("Shape : Square");
			// if(data[midx][midy]==-1)
			// 	output.add("Filled : 0");
			// else
			// 	output.add("Filled : 1");
			// output.add("Reflected : 0");
			// output.add("End Obj"+numObjs+" :");


			output.add("<figure index=\""+numObjs+"\">");
			output.add("<x> " + midx/8 + "</x>");
			output.add("<y>"+midy/8 +"</y>");
			output.add("<rotation> 0</rotation>");
			output.add("<size>"+size+"</size>");
			output.add("<shape>Square</shape>");
			if(data[midx][midy]==-1)
				output.add("<filled>0</filled>");
			else
				output.add("<filled>1</filled>");
			output.add("<reflected>0</reflected>");
			output.add("</figure>");



			for(int k = 0; k < i; k++)
			{
				for(int l = 0; l < i; l++)
				{
					data[x+k][y+l]=-1;
				}
			}
			return true;
		}
		return false;
	}
	
	public boolean square45(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = (x+x+i)/2;
		i=0;
		while(data[midx+i][y+i]!=-1)
		{
			i++;
		}
		int j = 0;
		while(data[midx-j][y+j]!=-1 && midx-j>0)
		{
			j++;
		}
		int size = (i*2)/8;
		
		while(data[midx+i-1][y+i]!=-1)
		{
			i++;
		}
		if(midx+j+1>=79 || y+j>=79)
			return false;
		while(data[midx+j+1][y+j]!=-1)
		{
			j++;
			if(midx+j+1 >=79 || y+j>=79)
				return false;
		}
		if(i-j>-2 && i-j<2 && size>2)
		{
			if(midx-i<0)
				return false;
			int midy = (y+y+i*2)/2;
			
			// output.add("Start Obj"+numObjs+" :");
			// output.add("X : " + midx/8);
			// output.add("Y : "+midy/8);
			// output.add("Rotation : 45");
			// output.add("Size : "+size);
			// output.add("Shape : Square");
			// if(data[midx][midy]==-1)
			// 	output.add("Filled : 0");
			// else
			// 	output.add("Filled : 1");
			// output.add("Reflected : 0");
			// output.add("End Obj"+numObjs+" :");


			output.add("<figure index=\""+numObjs+"\">");
			output.add("<x> " + midx/8 + "</x>");
			output.add("<y>"+midy/8 +"</y>");
			output.add("<rotation> 45</rotation>");
			output.add("<size>"+size+"</size>");
			output.add("<shape>Square</shape>");
			if(data[midx][midy]==-1)
				output.add("<filled>0</filled>");
			else
				output.add("<filled>1</filled>");
			output.add("<reflected>0</reflected>");
			output.add("</figure>");
			
			
			for(int k = 0; k < i*2; k++)
			{
				for(int l = 0; l < i*2; l++)
				{
					data[midx-i+k][y+l]=-1;
				}
			}
			return true;
		}
		return false;
	}
	
	public boolean circle(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
//		System.out.println(data[x][y]);
		if(data[x][y]==-1)
			return false;
		int i = 0;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = (x+x+i)/2;
		i=0;
		while(data[midx][y+i]!=-1)
		{
			i++;
		}
//		System.out.println("i" + i);
		if(i<12)
		{
			int temp = i;
			while(data[midx][y+i]==-1 && y+i<data.length-1)
			{
				i++;
			}
			while(data[midx][y+i]!=-1)
			{
				i++;
			}
			int size = i/8;
//			System.out.println("size " + size);
			if(size>2)
			{
//				System.out.println("inside circle " + numObjs);
//				if(numObjs<3)
//				{
//					for(int n = 0; n < data.length; n++)
//					{
//						System.out.println();
//						for(int m = 0; m < data.length; m++)
//						{
//							if(data[n][m]==-1)
//								System.out.print("-1       ");
//							else
//								System.out.print(data[n][m]);
//						}
//					}
//				}
				int midy = (y+y+i)/2;
				int j=0, k=0;
				while(data[midx+k][midy] == -1 && midx+k<data.length-1)
				{
					k++;
				}
				while(data[midx-j][midy] == -1 && midx-j>0)
				{
					j++;
				}
//				System.out.print("check ");
//				System.out.println((j+k+temp*2)-i);
				if((j+k+temp*2)-i>-3 && (j+k+temp*2)-i<3)
				{
					if(midx-j-temp+i>data.length-1)
						return false;
					
					if(midx-j-temp<0)
						return false;
					
					// output.add("Start Obj"+numObjs+" :");
					// output.add("X : " + midx/8);
					// output.add("Y : "+midy/8);
					// output.add("Rotation : 0");
					// output.add("Size : "+size);
					// output.add("Shape : Circle");
					// output.add("Filled : 0");
					// output.add("Reflected : 0");
					// output.add("End Obj"+numObjs+" :");

					output.add("<figure index=\""+numObjs+"\">");
					output.add("<x> " + midx/8 + "</x>");
					output.add("<y>"+midy/8 +"</y>");
					output.add("<rotation> 0</rotation>");
					output.add("<size>"+size+"</size>");
					output.add("<shape>Circle</shape>");
					output.add("<filled>0</filled>");
					output.add("<reflected>0</reflected>");
					output.add("</figure>");
					
					for(int l = 0; l <= i; l++)
					{
						for(int m = 0; m <= i; m++)
						{
							data[midx-j-temp+l][y+m]=-1;
						}
					}
					return true;
				}
			}
		}
		else
		{
			int size = (i+2)/8;
			if(size>2)
			{
				int midy = (y+y+i)/2;
				int j=0, k=0;
				
				if(data[midx+3][midy+2]==-1 || data[midx+3][midy-2]==-1)
					return false;
				
				while(data[midx+k][midy] != -1)
				{
					k++;
				}
				while(data[midx-j][midy] != -1)
				{
					j++;
				}
				if((j+k)-i>-2 && (j+k)-i<2)
				{
										
					// output.add("Start Obj"+numObjs+" :");
					// output.add("X : " + midx/8);
					// output.add("Y : "+midy/8);
					// output.add("Rotation : 0");
					// output.add("Size : "+size);
					// output.add("Shape : Circle");
					// output.add("Filled : 1");
					// output.add("Reflected : 0");
					// output.add("End Obj"+numObjs+" :");

					output.add("<figure index=\""+numObjs+"\">");
					output.add("<x> " + midx/8 + "</x>");
					output.add("<y>"+midy/8 +"</y>");
					output.add("<rotation> 0</rotation>");
					output.add("<size>"+size+"</size>");
					output.add("<shape>Circle</shape>");
					output.add("<filled>1</filled>");
					output.add("<reflected>0</reflected>");
					output.add("</figure>");
					
					for(int l = 0; l <= i; l++)
					{
						for(int m = 0; m <= i; m++)
						{
							data[midx-j+l][y+m]=-1;
						}
					}
					return true;
				}
			}
		}
		return false;
	}
	
	public boolean plus(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = (x+x+i)/2;
		i=0;
		int j = 0;
		while(data[midx-j][y]!=-1 && midx-j>0)
		{
			j++;
		}
		while(data[midx+i][y]!=-1)
		{
			i++;
		}

		if((j-i)>-2 && (j-i)<2)
		{
			int tempxi = midx+i-1;
			int tempxj = midx-j+1;
			i=0;
			j=0;
			while(data[tempxi][y+j]!=-1)
			{
				j++;
			}
			while(data[tempxi][y+i]!=-1)
			{
				i++;
			}
			if(i==j)
			{
				int tempy = y+i-1;
				j=0;
				i=0;
				while(data[tempxj-j][tempy]!=-1)
				{
					j++;
				}
				while(data[tempxi+i][tempy]!=-1)
				{
					i++;
				}
				int size = ((tempxi-1)-(tempxj+1))/8*2;
				if(i==j && size > 2)
				{
					if(midx-((tempxi-1)-(tempxj+1))<0)
						return false;
					if((midx-((tempxi-1)-(tempxj+1))+((tempxi-1)-(tempxj+1))*2)>=80)
					{
						return false;
					}
					
					if((y+(tempxi-1)-(tempxj+1))*2>=80)
					{
						return false;
					}
					
					int midy = y+((tempxi-1)-(tempxj+1));
					
					// output.add("Start Obj"+numObjs+" :");
					// output.add("X : " + midx/8);
					// output.add("Y : "+midy/8);
					// output.add("Rotation : 0");
					// output.add("Size : "+size);
					// output.add("Shape : Plus");
					// if(data[midx][midy]==-1)
					// 	output.add("Filled : 0");
					// else
					// 	output.add("Filled : 1");
					// output.add("Reflected : 0");
					// output.add("End Obj"+numObjs+" :");


					output.add("<figure index=\""+numObjs+"\">");
					output.add("<x> " + midx/8 + "</x>");
					output.add("<y>"+midy/8 +"</y>");
					output.add("<rotation> 0</rotation>");
					output.add("<size>"+size+"</size>");
					output.add("<shape>Plus</shape>");
					if(data[midx][midy]==-1)
						output.add("<filled>0</filled>");
					else
						output.add("<filled>1</filled>");
					output.add("<reflected>0</reflected>");
					output.add("</figure>");
					
					for(int m = 0; m <= ((tempxi-1)-(tempxj+1))*2; m++)
					{
						for(int n = 0; n <= ((tempxi-1)-(tempxj+1))*2; n++)
						{
							data[midx-((tempxi-1)-(tempxj+1))+m][y+n] = -1;
						}
					}
					return true;
				}
			}
		}
		return false;
	}
	
	public boolean triangle(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = (x+x+i)/2;
		i=0;
		while(data[midx][y+i]!=-1)
		{
			i++;
		}
		if(i<12)
		{
			while(data[midx][y+i]==-1 && y+i<data.length-1)
			{
				i++;
			}
			int boty = y+i;
			int j = 0;
			int k = 0;
			while(data[midx+k][boty]!=-1)
			{
				k++;
			}
			while(data[midx-j][boty]!=-1 && midx-j>0)
			{
				j++;
			}
			int size = (j+k)/8;
			if(j==k && size > 2)
			{
				int midy = (y+boty+5)/2;
				
				// output.add("Start Obj"+numObjs+" :");
				// output.add("X : " + midx/8);
				// output.add("Y : "+midy/8);
				// output.add("Rotation : 0");
				// output.add("Size : "+size);
				// output.add("Shape : Triangle");
				// output.add("Filled : 0");
				// output.add("Reflected : 0");
				// output.add("End Obj"+numObjs+" :");

				output.add("<figure index=\""+numObjs+"\">");
				output.add("<x> " + midx/8 + "</x>");
				output.add("<y>"+midy/8 +"</y>");
				output.add("<rotation> 0</rotation>");
				output.add("<size>"+size+"</size>");
				output.add("<shape>Triangle</shape>");
				output.add("<filled>0</filled>");
				output.add("<reflected>0</reflected>");
				output.add("</figure>");
				
				for(int m = 0; m <= j+k; m++)
				{
					for(int n = 0; n <= i+5; n++)
					{
						data[midx-j+m][y+n]=-1;
					}
				}
				return true;
			}
		}
		else
		{
			int boty = y+i-1;
			int j = 0;
			int k = 0;
			while(data[midx+k][boty]!=-1)
			{
				k++;
			}
			while(data[midx-j][boty]!=-1)
			{
				j++;
			}
			int size = (j+k)/8;
			if((j-k)<2 && (j-k)>-2 && size >= 2)
			{
				int midy = (y+boty)/2;
				
				// output.add("Start Obj"+numObjs+" :");
				// output.add("X : " + midx/8);
				// output.add("Y : "+midy/8);
				// output.add("Rotation : 0");
				// output.add("Size : "+size);
				// output.add("Shape : Triangle");
				// output.add("Filled : 1");
				// output.add("Reflected : 0");
				// output.add("End Obj"+numObjs+" :");


				output.add("<figure index=\""+numObjs+"\">");
				output.add("<x> " + midx/8 + "</x>");
				output.add("<y>"+midy/8 +"</y>");
				output.add("<rotation> 0</rotation>");
				output.add("<size>"+size+"</size>");
				output.add("<shape>Triangle</shape>");
				output.add("<filled>1</filled>");
				output.add("<reflected>0</reflected>");
				output.add("</figure>");
				
				for(int m = 0; m <= j+k; m++)
				{
					for(int n = 0; n <= i; n++)
					{
						data[midx-j+m][y+n]=-1;
					}
				}
				return true;
			}
		}
		return false;
	}
	
	public boolean pacman(int[][] data, int x, int y, ArrayList<String> output, int numObjs)
	{
		if(data[x][y]==-1)
			return false;
		int i = 0;
		boolean found = false;
		while(data[x+i][y]!=-1)
		{
			i++;
		}
		int midx = x+i-3;
		int xr = x+i-1;
		i=0;
		while(data[xr][y+i]!=-1 && data[xr+1][y+i]==-1)
		{
			i++;
		}
		int j = i+3;
		int midy = y+i+1;
		if(data[xr][y+j]==-1)
		{
			while(data[xr][y+j]==-1 && ((y+j)<data.length-1))
			{
				j++;
			}
			int temp = j-i;
			if(temp-i<2 && temp-i>-2)
			{
				temp = 0;
				while(data[xr+temp][midy]!=-1)
				{
					temp++;
				}
				if(temp>7)
				{
					int size = (j+3)/8;
					// output.add("Start Obj"+numObjs+" :");
				 //    output.add("X : " + midx/8);
				 //    output.add("Y : "+midy/8);
				 //    output.add("Rotation : 0");
				 //    output.add("Size : "+size);
					// output.add("Shape : Pacman");
					// output.add("Filled : 0");
					// output.add("Reflected : 0");
					// output.add("End Obj"+numObjs+" :");

					output.add("<figure index=\""+numObjs+"\">");
					output.add("<x> " + midx/8 + "</x>");
					output.add("<y>"+midy/8 +"</y>");
					output.add("<rotation> 0</rotation>");
					output.add("<size>"+size+"</size>");
					output.add("<shape>Pacman</shape>");
					output.add("<filled>0</filled>");
					output.add("<reflected>0</reflected>");
					output.add("</figure>");
					
					found = true;
					for(int m = 0; m <= (midy-y)*2+2; m++)
					{
						for(int n = 0; n <= (midy-y)*2+2; n++)
						{
							data[midx-(midy-y)+m][y+n]=-1;
						}
					}
					return true;
				}				
			}
		}
		else
		{
			while(data[xr][y+j]!=-1)
			{
				j++;
			}
			int temp = j-i-3;
			if(temp-i<2 && temp-i>-2)
			{
				temp = 0;
				while(data[xr+temp][midy]!=-1)
				{
					temp++;
				}
				if(temp>7)
				{
					int size = (j+3)/8;
					found = true;
					
					// output.add("Start Obj"+numObjs+" :");
				 //    output.add("X : " + midx/8);
				 //    output.add("Y : "+midy/8);
				 //    output.add("Rotation : 0");
				 //    output.add("Size : "+size);
					// output.add("Shape : Pacman");
					// output.add("Filled : 1");
					// output.add("Reflected : 0");
					// output.add("End Obj"+numObjs+" :");

					output.add("<figure index=\""+numObjs+"\">");
					output.add("<x> " + midx/8 + "</x>");
					output.add("<y>"+midy/8 +"</y>");
					output.add("<rotation> 0</rotation>");
					output.add("<size>"+size+"</size>");
					output.add("<shape>Pacman</shape>");
					output.add("<filled>1</filled>");
					output.add("<reflected>0</reflected>");
					output.add("</figure>");
					
					for(int m = 0; m <= (midy-y)*2+2; m++)
					{
						for(int n = 0; n <= (midy-y)*2+2; n++)
						{
							data[midx-(midy-y)+m][y+n]=-1;
						}
					}
					return true;
				}				
			}
		}
		if(!found)
		{
			midx = x+1;
			int xl = x;
			i=0;
			if(xl < 1)
				return false;
			while(data[xl][y+i]!=-1 && data[xl-1][y+i]==-1)
			{
				i++;
			}
			j = i+3;
			midy = y+i+1;
			if(data[xl][y+j]==-1)
			{
				while(data[xl][y+j]==-1 && y+j < data.length-1)
				{
					j++;
				}
				int temp = j-i;
				if(temp-i<2 && temp-i>-2)
				{
					temp = 0;
					while(data[xl-temp][midy]!=-1)
					{
						temp++;
					}
					if(temp>7)
					{
						int size = (j+3)/8;
												
						// output.add("Start Obj"+numObjs+" :");
					 //    output.add("X : " + midx/8);
					 //    output.add("Y : "+midy/8);
					 //    output.add("Rotation : 0");
					 //    output.add("Size : "+size);
						// output.add("Shape : Pacman");
						// output.add("Filled : 0");
						// output.add("Reflected : 1");
						// output.add("End Obj"+numObjs+" :");

						output.add("<figure index=\""+numObjs+"\">");
						output.add("<x> " + midx/8 + "</x>");
						output.add("<y>"+midy/8 +"</y>");
						output.add("<rotation> 0</rotation>");
						output.add("<size>"+size+"</size>");
						output.add("<shape>Pacman</shape>");
						output.add("<filled>0</filled>");
						output.add("<reflected>1</reflected>");
						output.add("</figure>");
						
						found = true;
						for(int m = 0; m <= (midy-y)*2+2; m++)
						{
							for(int n = 0; n <= (midy-y)*2+2; n++)
							{
								data[midx-(midy-y)+m][y+n]=-1;
							}
						}
						return true;
					}				
				}
			}
			else
			{
				while(data[xl][y+j]!=-1)
				{
					j++;
				}
				int temp = j-i-3;
				if(temp-i<2 && temp-i>-2)
				{
					temp = 0;
					while(data[xl-temp][midy]!=-1)
					{
						temp++;
					}
					if(temp>7)
					{
						int size = (j+3)/8;
						found = true;
						
						// output.add("Start Obj"+numObjs+" :");
					 //    output.add("X : " + midx/8);
					 //    output.add("Y : "+midy/8);
					 //    output.add("Rotation : 0");
					 //    output.add("Size : "+size);
						// output.add("Shape : Pacman");
						// output.add("Filled : 1");
						// output.add("Reflected : 1");
						// output.add("End Obj"+numObjs+" :");


						output.add("<figure index=\""+numObjs+"\">");
						output.add("<x> " + midx/8 + "</x>");
						output.add("<y>"+midy/8 +"</y>");
						output.add("<rotation> 0</rotation>");
						output.add("<size>"+size+"</size>");
						output.add("<shape>Pacman</shape>");
						output.add("<filled>1</filled>");
						output.add("<reflected>1</reflected>");
						output.add("</figure>");
						
						for(int m = 0; m <= (midy-y)*2+2; m++)
						{
							for(int n = 0; n <= (midy-y)*2+2; n++)
							{
								data[midx-(midy-y)+m][y+n]=-1;
							}
						}
						return true;
					}				
				}
			}
		}
		if(!found)
		{
			i = 0;
			while(data[x+i][y]!=-1)
			{
				i++;
			}
			midx=(x+x+i)/2;
			i = 0;
			while(data[midx][y+i]!=-1)
			{
				i++;
			}
			if(i<12)
			{
				while(data[midx][y+i]==-1 && y+i < data.length-1)
				{
					i++;
				}
				midy = y+i+1;
				j = i;
				while(data[midx][y+j]!=-1)
				{
					j++;
				}
				j-=3;
				if((((j-i)-i)<2) && (((j-i)-i)>-2))
				{
					int l = 0;
					while(data[midx+l][midy]!=-1)
					{
						l++;
					}
					if(l>7)
					{
						int size = (j+3)/8;
						found = true;
						
						// output.add("Start Obj"+numObjs+" :");
					 //    output.add("X : " + midx/8);
					 //    output.add("Y : "+midy/8);
					 //    output.add("Rotation : 270");
					 //    output.add("Size : "+size);
						// output.add("Shape : Pacman");
						// output.add("Filled : 0");
						// output.add("Reflected : 0");
						// output.add("End Obj"+numObjs+" :");

						output.add("<figure index=\""+numObjs+"\">");
						output.add("<x> " + midx/8 + "</x>");
						output.add("<y>"+midy/8 +"</y>");
						output.add("<rotation> 270</rotation>");
						output.add("<size>"+size+"</size>");
						output.add("<shape>Pacman</shape>");
						output.add("<filled>0</filled>");
						output.add("<reflected>0</reflected>");
						output.add("</figure>");
						
						for(int m = 0; m <= (midy-y)*2+2; m++)
						{
							for(int n = 0; n <= (midy-y)*2+2; n++)
							{
								data[midx-(midy-y)+m][y+n]=-1;
							}
						}
						return true;
					}
				}
			}
			else
			{
				i = 0;
				while(data[midx][y+i]!=-1 && data[midx+3][y+i] != -1)
				{
					i++;
				}
				j = i;
				while(data[midx][y+j]!=-1 && data[midx+3][y+j] == -1)
				{
					j++;
				}
				i-=2;
				midy = y+i;
				if((((j-i)-i)<2) && (((j-i)-i)>-2))
				{
					int l = 0;
					while(data[midx+l][midy]!=-1)
					{
						l++;
					}
					if(l>7)
					{
						int size = (j+3)/8;
						found = true;
						
						// output.add("Start Obj"+numObjs+" :");
					 //    output.add("X : " + midx/8);
					 //    output.add("Y : "+midy/8);
					 //    output.add("Rotation : 270");
					 //    output.add("Size : "+size);
						// output.add("Shape : Pacman");
						// output.add("Filled : 1");
						// output.add("Reflected : 0");
						// output.add("End Obj"+numObjs+" :");

						output.add("<figure index=\""+numObjs+"\">");
						output.add("<x> " + midx/8 + "</x>");
						output.add("<y>"+midy/8 +"</y>");
						output.add("<rotation> 270</rotation>");
						output.add("<size>"+size+"</size>");
						output.add("<shape>Pacman</shape>");
						output.add("<filled>1</filled>");
						output.add("<reflected>0</reflected>");
						output.add("</figure>");
						
						for(int m = 0; m <= (midy-y)*2+2; m++)
						{
							for(int n = 0; n <= (midy-y)*2+2; n++)
							{
								data[midx-(midy-y)+m][y+n]=-1;
							}
						}
						return true;
					}
				}
			}
		}
		if(!found)
		{
			i = 0;
			while(data[x+i][y]!=-1)
			{
				i++;
			}
			midx=(x+x+i)/2;
			i = 0;
			while(data[midx][y+i]!=-1)
			{
				i++;
			}
			if(i<12)
			{
				while(data[midx][y+i]==-1 && y+i<data.length-1)
				{
					i++;
				}
				midy = y+i+1;
				j = i;
				while(data[midx][y+j]!=-1)
				{
					j++;
				}
				j-=3;
				if((((j-i)-i)<2) && (((j-i)-i)>-2))
				{
					int l = 0;
					while(data[midx-l][midy]!=-1)
					{
						l++;
					}
					if(l>7)
					{
						int size = (j+3)/8;
						found = true;
						
						// output.add("Start Obj"+numObjs+" :");
					 //    output.add("X : " + midx/8);
					 //    output.add("Y : "+midy/8);
					 //    output.add("Rotation : 270");
					 //    output.add("Size : "+size);
						// output.add("Shape : Pacman");
						// output.add("Filled : 0");
						// output.add("Reflected : 1");
						// output.add("End Obj"+numObjs+" :");

						output.add("<figure index=\""+numObjs+"\">");
						output.add("<x> " + midx/8 + "</x>");
						output.add("<y>"+midy/8 +"</y>");
						output.add("<rotation> 270</rotation>");
						output.add("<size>"+size+"</size>");
						output.add("<shape>Pacman</shape>");
						output.add("<filled>0</filled>");
						output.add("<reflected>1</reflected>");
						output.add("</figure>");
						
						for(int m = 0; m <= (midy-y)*2+2; m++)
						{
							for(int n = 0; n <= (midy-y)*2+2; n++)
							{
								data[midx-(midy-y)+m][y+n]=-1;
							}
						}
						return true;
					}
				}
			}
			else
			{
				i = 0;
				while(data[midx][y+i]!=-1 && data[midx-3][y+i] != -1)
				{
					i++;
				}
				j = i;
				while(data[midx][y+j]!=-1 && data[midx-3][y+j] == -1)
				{
					j++;
				}
				i-=2;
				midy = y+i;
				if((((j-i)-i)<2) && (((j-i)-i)>-2))
				{
					int l = 0;
					while(data[midx+l][midy]!=-1)
					{
						l++;
					}
					if(l>7)
					{
						int size = (j+3)/8;
						found = true;
						
						// output.add("Start Obj"+numObjs+" :");
					 //    output.add("X : " + midx/8);
					 //    output.add("Y : "+midy/8);
					 //    output.add("Rotation : 270");
					 //    output.add("Size : "+size);
						// output.add("Shape : Pacman");
						// output.add("Filled : 1");
						// output.add("Reflected : 1");
						// output.add("End Obj"+numObjs+" :");

						output.add("<figure index=\""+numObjs+"\">");
						output.add("<x> " + midx/8 + "</x>");
						output.add("<y>"+midy/8 +"</y>");
						output.add("<rotation> 270</rotation>");
						output.add("<size>"+size+"</size>");
						output.add("<shape>Pacman</shape>");
						output.add("<filled>1</filled>");
						output.add("<reflected>1</reflected>");
						output.add("</figure>");
						
						for(int m = 0; m <= (midy-y)*2+2; m++)
						{
							for(int n = 0; n <= (midy-y)*2+2; n++)
							{
								data[midx-(midy-y)+m][y+n]=-1;
							}
						}
						return true;
					}
				}
			}
		}
		return false;
	}
}
