package org.h2.api;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Quartile implements AggregateFunction {
	private List<Integer> numbers = new ArrayList<>();
	private Double[] result = new Double[3]; // Stores the final result

	@Override
	public void init(java.sql.Connection cnctn) throws java.sql.SQLException {
	}

	@Override
	public int getType(int[] inputTypes) throws SQLException {
		// TODO Auto-generated method stub
		return inputTypes[0];
	}

	@Override
	public void add(Object value) throws SQLException {
		// TODO Auto-generated method stub
		numbers.add((Integer) value);
	}

	@Override
	public Object getResult() throws SQLException {
		// TODO Auto-generated method stub
		int[] nums = numbers.stream().mapToInt(Integer::intValue).toArray();
		Arrays.sort(nums);
		if (nums.length % 2 == 0) {
			result[1] = ((double) nums[nums.length / 2] + (double) nums[nums.length / 2 - 1]) / 2;
			int splitAt = nums.length / 2;
			result[0] = calculateQuartile(subArray(nums, 0, splitAt));
			result[2] = calculateQuartile(subArray(nums, splitAt, nums.length));
		} else {
			result[1] = (double) nums[nums.length / 2];
			int splitForEndFQ = nums.length/2;
			int splitForBeginTQ = nums.length/2 + 1;
			result[0] = calculateQuartile(subArray(nums, 0, splitForEndFQ));
			result[2] = calculateQuartile(subArray(nums, splitForBeginTQ, nums.length));
		}
		return result;
	}

	public static <T> int[] subArray(int[] array, int beg, int end) {
		System.out.println(Arrays.toString(Arrays.copyOfRange(array, beg, end)));
		return Arrays.copyOfRange(array, beg, end);
	}

	private Double calculateQuartile(int[] nums) {
		if (nums.length % 2 == 0)
			return ((double) nums[nums.length / 2] + (double) nums[nums.length / 2 - 1]) / 2;
		else
			return (double) nums[nums.length / 2];
	}

}
