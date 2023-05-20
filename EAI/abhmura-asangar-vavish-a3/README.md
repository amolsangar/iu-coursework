# Assignment 3: Probability and Statistical Learning

## **Part 1 (Part-of-speech tagging - Vaibhav Vishwanath)** ##
  

## **Part 2 (Ice tracking - Amol Sangar)** ##
- The problem is to trace two ice lines on the image using different approaches like Bayes net, HMM with Viterbi and human feedback.
- The first technique is to use Bayes Net in its simplest form. Here we can see that the approach performs averagely and misses out many points on the edge. It can also be seen in some cases (like test image 23) that the edge points are dispersed all over the image and thus leads to non-uniform edge trace.
- The second technique uses HMM with Viterbi algorithm which handles the drawback from above efficiently. The Viterbi algorithm helps in tweaking the transition probabilities and gives more weightage to edge points which are in vicinity of previous edge points. This leads in forming a uniform trace line and can be observed as well.
- The final technique uses feedback points from a human. Since these points are assumed to be on the trace line, we can enhance the algorithm to only consider this feedback point on the column. Thus, this technique can use multiple such points to improve the final result. 
  
  In human feedback, the edge strength in the points column except the mentioned point is reduced to zero in order to make the trace line pass through the feedback point only.
  
  **Emission and transition probabilities:**
- The emission probabilities are calculated from the edge strength matrix where higher values mean an edge is present. The transition probabilities are calculated per pixel and looks for previous columns closest 15 pixels and assigns higher weightage to them. This leads to a uniform line tracing as mentioned earlier.
    
  ### **Output:** ###
  
  **Test Image 23**

  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_23/output_simple.jpg' alt='Output Simple'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_23/output_hmm.jpg' alt='Output Image'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_23/output_feedback.jpg' alt='Output Image'>
  <br/>
  Simple &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; HMM with Viterbi &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Human Feedback
  
  **Test Image 09**
  
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_09/output_simple.jpg' alt='Output Simple'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_09/output_hmm.jpg' alt='Output HMM'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_09/output_feedback.jpg' alt='Output Human Feedback'>
  <br/>
  Simple &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; HMM with Viterbi &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Human Feedback
  
  **Test Image 16**
  
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_16/output_simple.jpg' alt='Output Simple'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_16/output_hmm.jpg' alt='Output HMM'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_16/output_feedback.jpg' alt='Output Human Feedback'>
  <br/>
  Simple &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; HMM with Viterbi &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Human Feedback
  
  **Test Image 30**
  
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_30/output_simple.jpg' alt='Output Simple'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_30/output_hmm.jpg' alt='Output HMM'>
  <img src='https://github.com/amolsangar/iu-coursework/blob/main/EAI/abhmura-asangar-vavish-a3/part2/output/image_30/output_feedback.jpg' alt='Output Human Feedback'>
  <br/>
  Simple &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; HMM with Viterbi &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Human Feedback
  
  **Test Image 31**
  
  <img src='https://github.iu.edu/cs-b551-fa2021/abhmura-asangar-vavish-a3/blob/master/part2/output/image_31/output_simple.jpg' alt='Output Simple'>
  <img src='https://github.iu.edu/cs-b551-fa2021/abhmura-asangar-vavish-a3/blob/master/part2/output/image_31/output_hmm.jpg' alt='Output HMM'>
  <img src='https://github.iu.edu/cs-b551-fa2021/abhmura-asangar-vavish-a3/blob/master/part2/output/image_31/output_feedback.jpg' alt='Output Human Feedback'>
  <br/>
  Simple &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; HMM with Viterbi &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Human Feedback


   
## **Part 3 (Reading text - Abhijeet Sridhar M)** ##
