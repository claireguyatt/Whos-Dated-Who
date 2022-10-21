// Oct 20
// used solution

import java.util.*;

class Program {

  public int[] nextGreaterElement(int[] array) {

    if (array.length == 0) {
      return new int[0];
    }

    // array to return
    int[] nextGreatests = new int[array.length];
    Arrays.fill(nextGreatests, -1);

    // stack that keeps index of next biggest number at the top
    Stack<Integer> stack = new Stack<Integer>();
    
    // iterate through input array and add elements to the stack until
    // greater than element is reached
    for (int i=0; i<array.length*2; i++) {

      int circularIndex = i%array.length;

      while (!stack.isEmpty() && array[stack.peek()] < array[circularIndex]) {
        
        int index = stack.pop();
        nextGreatests[index] = array[circularIndex];

      }
      // if the stack is empty or the current num is no longer
      // greater than those on the stack, add current index
      stack.push(circularIndex);
    }
    
    return nextGreatests;
  }
}

