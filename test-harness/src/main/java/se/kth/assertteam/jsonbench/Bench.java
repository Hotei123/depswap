package se.kth.assertteam.jsonbench;

import se.kth.assertteam.jsonbench.parser.GsonParser;
import se.kth.assertteam.jsonbench.parser.JsonSimple;
import se.kth.assertteam.jsonbench.parser.OrgJSON;
import se.kth.assertteam.jsonbench.parser.ResultReport;

import javax.xml.transform.Result;
import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.*;
import java.util.stream.Collectors;

public class Bench {
	public static void main(String[] args) throws IOException {

		JP orgJson = new OrgJSON();
		test(orgJson);

		JP gson = new GsonParser();
		test(gson);

		JP simple = new JsonSimple();
		test(simple);
	}

	public static void test(JP parser) throws IOException {
		File correct = new File("../data/bench/correct");
		File errored = new File("../data/bench/errored");
		File undefined = new File("../data/bench/undefined");
		System.out.println("Start testing " + parser.getName());
		printResults(parser, "correct", testAllCorrectJson(correct, parser));
		printResults(parser, "errored", testAllIncorrectJson(errored, parser));
		printResults(parser, "undefined", testAllCorrectJson(undefined, parser));

	}

	public static void printResults(JP parser, String category, Map<String,ResultReport> results) throws IOException {
		File dir = new File("results");
		File output = new File(dir,parser.getName() + "_" + category + "_results.csv");
		System.out.println("Print result from " + parser.getName() + " to " + output.getName());
		if(output.exists()) {
			output.delete();
		}
		output.createNewFile();
		String headerString = "Parser,Category,File,Result,MemoryUsed\n";
		try {
			Files.write(output.toPath(), "Parser,Category,File,Result,MemoryUsed\n".getBytes(), StandardOpenOption.APPEND);
		} catch (IOException e) {
			e.printStackTrace();
		}
		results.forEach((k,v) -> {
			String line = parser.getName() + "," + category + "," + k + "," + v.kind +  "," +
					Long.toString(v.memoryUsedList.get(0)) + "\n";
			try {
				Files.write(output.toPath(), line.getBytes(), StandardOpenOption.APPEND);
			} catch (IOException e) {
				e.printStackTrace();
			}
		});
	}

	public static List<File> findFiles(String dir, String suffix) throws IOException {
		List<File> files = new ArrayList<>();

		Files.walk(Paths.get(dir))
				.filter(Files::isRegularFile)
				.forEach((f)->{
					String file = f.toString();
					if( file.endsWith(suffix))
						files.add(new File(file));
				});

		return files;
	}

	public static String readFile(File f) throws IOException {
		return Files.lines(f.toPath(), StandardCharsets.UTF_8).collect(Collectors.joining("\n"));
	}

	public static Map<String,ResultReport> testAllCorrectJson(File inDir, JP parser) throws IOException {
		Map<String,ResultReport> resultLabels = new HashMap<>();
		for(File f: findFiles(inDir.getAbsolutePath(),".json")) {
			resultLabels.put(f.getName(), testCorrectJson(f, parser));
		}
		return resultLabels;
	}

	public static Map<String,ResultReport> testAllIncorrectJson(File inDir, JP parser) throws IOException {
		Map<String,ResultReport> resultLabels = new HashMap<>();
		for(File f: findFiles(inDir.getAbsolutePath(),".json")) {
			resultLabels.put(f.getName(), testIncorrectJson(f, parser));
		}
		return resultLabels;
	}

	public static ResultReport testCorrectJson(File f, JP parser)  {
		String jsonIn = null;
		ResultReport resultFile = new ResultReport();
		Runtime runtime = Runtime.getRuntime();
		long freeMemory_0;
		ArrayList<Long> memoryUsedList = resultFile.memoryUsedList;
		try {
			for (int i = 0; i < resultFile.memoryUsedList.size(); i++) {
				freeMemory_0 = runtime.freeMemory();
				jsonIn = readFile(f);
				resultFile.memoryUsedList.set(i, freeMemory_0 - runtime.freeMemory());
			}
		} catch (Exception e) {
			resultFile.kind = ResultKind.FILE_ERROR;
			return resultFile;
		}
		Object jsonObject = null;
		String jsonOut;
		try {
			try {
				jsonObject = parser.parseString(jsonIn);
				if(jsonObject == null) {
					resultFile.kind = ResultKind.NULL_OBJECT;
					return resultFile;
				}
			} catch (Exception e) {
				resultFile.kind = ResultKind.PARSE_EXCEPTION;
				return resultFile;
			}
			if(jsonObject != null) {
				try {
					jsonOut = parser.print(jsonObject);
					if(jsonOut.equalsIgnoreCase(jsonIn)) {
						resultFile.setPerformance(ResultKind.OK, memoryUsedList);
						return resultFile;
					}
					if(parser.equivalence(jsonObject,parser.parseString(jsonOut))) {
						resultFile.kind = ResultKind.EQUIVALENT_OBJECT;
					} else {
						resultFile.kind = ResultKind.NON_EQUIVALENT_OBJECT;
					}
					return resultFile;
				} catch (Exception e) {
					resultFile.kind = ResultKind.PRINT_EXCEPTION;
					return resultFile;
				}
			}
		} catch (Error e) {
			resultFile.kind = ResultKind.CRASH;
			return resultFile;
		}
		return null;
	}

	public static ResultReport testIncorrectJson(File f, JP parser)  {
		ResultReport resultFile = new ResultReport();
		String jsonIn = null;
		Runtime runtime = Runtime.getRuntime();
		long freeMemory_0;
		try {
			for (int i = 0; i < resultFile.memoryUsedList.size(); i++) {
				freeMemory_0 = runtime.freeMemory();
				jsonIn = readFile(f);
				resultFile.memoryUsedList.set(i, freeMemory_0 - runtime.freeMemory());
			}
		} catch (Exception e) {
			resultFile.kind = ResultKind.FILE_ERROR;
			return resultFile;
		}
		try {
			Object jsonObject = null;
			String jsonOut;
			try {
				try {
					jsonObject = parser.parseString(jsonIn);
					if (jsonObject != null)
						resultFile.kind = ResultKind.UNEXPECTED_OBJECT;
					else
						resultFile.kind = ResultKind.NULL_OBJECT;
					return resultFile;
				} catch (Exception e) {
					resultFile.kind = ResultKind.OK;
					return resultFile;
				}
			} catch (Error e) {
				resultFile.kind = ResultKind.CRASH;
				return resultFile;
			}
		} catch (Exception e) {
			return null;
		}
	}
	//read file
	//get jsons
	//parse test
	//print test
}
