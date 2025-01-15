# An Assessment of 5 Main Websites with World Flags

## Intro
Flags of the world (flags of countries, states, territories, etc.) are commonly used. There are numerous online sources for them in the form of image files, and for a separate project I had to assess what source was better, or at least more suitable for my needs. The interest is **not** in which countries are included in each source, which is straightforward, but in **the differences in the flags for a given country**, and here I present the main results.

The sources I evaluated are:
1. [Country-Flags](https://github.com/hampusborgos/country-flags), a GitHub repository that claims to contain *accurate renders of all the worlds flags in SVG and PNG format*, **CF**.
2. [Encyclopedia Britannica (students)](https://kids.britannica.com/students/article/flags-of-the-world/274335), **EB**.
3. The CIA's [World FactBook](https://www.cia.gov/the-world-factbook/references/flags-of-the-world/), **FB**.
4. The [Wikipedia](https://en.m.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states), **WK**.
5. Worldodometer for [countries](https://www.worldometers.info/geography/flags-of-the-world/) and [dependent territories](https://www.worldometers.info/geography/flags-of-dependent-territories/), **WO**.


The assessment compares the relative performance of the sources along the following criteria:
 - Number of flags
 - Size and aspect ratio
 - Color

The main scripts I have used, in python, are included in the folder *./scripts*; the images, flags and results, are in *./IMG*.

I use the [ISO alpha-3 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) for the identification of the countries (I retain XKX for Kosovo and add EUR for the European Union; entities without iso-3 code, e.g. Wales, are not included). With regard to names, I generally follow the criteria used in the GitHub repository [Country Codes](https://github.com/datasets/country-codes).

## File downloading
Script *100_flags_get_R0.py* downloads the files from the five sites. It uses *requests* with the support of *BeautifulSoup*.
The formats of the scraped images are:
- CF: SVG
- EB: JPG
- FB: JPG
- WK: SVG
- WO: GIF

[Note: I found too many difficulties to install/use the library *Cairo*, or wrappers, to operate with the SVGs, so I manually (off-script, online) converted them to PNGs (100% quality, width=1000 px) with [Pixelied](https://pixelied.com/convert/svg-converter/svg-to-png).]
 
## Number of flags
The comparison of the sources by the number of flags is slightly skewed because not all have the same scope, which in all cases should include the internationally recognized states. The range varies between 196 (EB) and 251 (CF) flags.
The attached diagram shows the quantitative relationships among the sources, while **this csv file** provides the details.
[![countries-flags-R0.png](https://i.postimg.cc/sxhc73JW/countries-flags-R0.png)](https://postimg.cc/p5Pztb4V)

Script *120_flags_show_R0.py* plots the versions of the flags per country in an arrangement that facilitates the comparisons among sources. The printout results are included in folder *./120PNG*, and a couple of them can be seen here:
[![ARG](https://i.postimg.cc/kM8zXHK3/ARG.png)](https://postimg.cc/QV80f0f0)
[![ZAF](https://i.postimg.cc/7YkcCNnC/ZAF.png)](https://postimg.cc/grg4Q85d)

## Size and aspect ratio
One might expect the representation of the flag sizes to be a rather dull chart, but there are some nuances as shown in the following box-plot that presents the distribution of flag width:
[![flag-sizes.png](https://i.postimg.cc/C1vtmMD6/flag-sizes.png)](https://postimg.cc/vgV3ms0W)
Britannica sets a strict dimensional constraint, the World FactBook has a wider range, rather mirrored by Worldodometer, while Country-Flags and Wikipedia (both with SVG format) have far larger ranges, nearly wild in the case of CF: from 3 to almost 220,000 pixels!

[Note: although SVG files are scalable without change, they include in their description a parameter related to their *dimensions*, either viewbox or width and height, which is from where I extracted the values used in the precedent chart.]

Also one would expect that the aspect ratio (width/height) for a given country did not change across the sources. But here are the results using as reference the aspect ratios of Country-Flags:
[![aspect-ratios.png](https://i.postimg.cc/JhwCwhsy/aspect-ratios.png)](https://postimg.cc/qNG5y4X0)
For sources other than Wikipedia, roughly 20% of the flags have an aspect ratio that differs more than ±10% of the reference value, and even the Encyclopedia Britannica has nearly 5% of the flags 10% narrower than the reference. Also here Worldodometer mimics the World FactBook.
Although the average and median are centered around zero, the number of outliers is surprisingly large.

## Color
I have computed the normalized color histogram for each flag, in RGB space. This is simply done by counting the number of pixels of each color taking into consideration the total number of pixels in the image. 

This measure combines two separate aspects: differences in color, and differences in the areas associated to each color. It is clearly not a perfect measure, but it is intuitive enough and separates the color dimensions. My comparison does also not consider aspects as the representation of the coat of arms, just the quantitative use of colors. I considered other measures of image difference as [SSMI](https://en.wikipedia.org/wiki/Structural_similarity_index_measure), but thought it was not as clear.

The task is done by the script *180_flags_color_R0.py* and the results are in *./180PNG*, with two examples here. The chart on the left is a 3d histogram and represents the frequency of each RGB color, associated to the size of the bubble; the chart on the right shows a measure of error for each color band and the sum of the three, using as reference the image of Country-Flags. 

[Note: The error on each color band is computed as the Euclidean distance on the cumulated frequency distribution of color intensity between a given image and the reference, normalized. The total error is the sum of the errors on each color band.]
[![ARG.png](https://i.postimg.cc/0jr3tK96/ARG.png)](https://postimg.cc/ZvtVnRBZ)
[![ZAF.png](https://i.postimg.cc/fyFP1Wb8/ZAF.png)](https://postimg.cc/wRXFmpLN)

The differences among the sources are amazing, as already presented in the comparison of representations, but here it is also possible to identify the extent of transition colors. The pairs  World FactBook/Worldodometer and  Country-Flags/Wikipedia are also fairly clear.
This is shown in the following scatter plot that compares the total errors:
[![err-corr.png](https://i.postimg.cc/K8hqTH33/err-corr.png)](https://postimg.cc/PPKQsK4d)

Finally, the distribution of the frequency of errors (with CF as reference!) shows the comparative quality of the sources on the color domain, clearly ordered: [CF] > WK > EB >> FB > WO.
[![err-cum.png](https://i.postimg.cc/MKS3MLQM/err-cum.png)](https://postimg.cc/t7BN82Dp)

