package se.kth.assertteam.depswap;

import org.apache.maven.model.Dependency;
import org.apache.maven.model.Model;
import org.apache.maven.model.io.xpp3.MavenXpp3Reader;
import org.apache.maven.model.io.xpp3.MavenXpp3Writer;
import org.codehaus.plexus.util.xml.pull.XmlPullParserException;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.io.FileUtils;

public class Project {

	public static void main(String[] args) throws IOException {
		if(args.length < 4) {
			System.err.println("Usage: java -jar myjar.jar projectDir g:a:v g:a:v /path/to/libs ?r");
			System.exit(-1);
		}
		String projectDir = args[0];
		String targetedGAV = args[1];
		String replacementGAV = args[2];
		String pathToJars = args[3];

		if(args.length == 5) {
			//Restore
			for (File pom : findFiles(projectDir, "/old_pom.xml")) {
				File savedPom = new File(pom.getParentFile(), "pom.xml");
				FileUtils.deleteQuietly(savedPom);
				FileUtils.moveFile(pom, savedPom);
			}
		} else {
			for (File pom : findFiles(projectDir, "/pom.xml")) {
				File savedPom = new File(pom.getParentFile(), "old_pom.xml");
				FileUtils.deleteQuietly(savedPom);
				FileUtils.moveFile(pom, savedPom);
				String[] tgav = targetedGAV.split(":");
				String[] rgav = replacementGAV.split(":");
				try {
					swapDependency(
							savedPom, new File(savedPom.getParentFile(), "pom.xml"),
							tgav[0], tgav[1], (tgav[2].equals("*") ? null : tgav[2]),
							rgav[0], rgav[1], rgav[2],
							pathToJars
					);
				} catch (TransformationFailedException e) {
					System.out.println("Pom: " + pom.getPath() + " does not include the targeted dependency. Restoring original pom.");
					FileUtils.moveFile(savedPom, pom);
				}
			}
		}
	}

	public static List<File> findFiles(String dir, String filename) throws IOException {
		List<File> poms = new ArrayList<>();

		Files.walk(Paths.get(dir))
			.filter(Files::isRegularFile)
			.forEach((f)->{
				String file = f.toString();
				if( file.endsWith(filename))
					poms.add(new File(file));
			});

		return poms;
	}

	//find all poms
	//for each replace the json dep with replacement lib (bridge, facade, implem

	public static void swapDependency(File inPomFile, File outPomFile,
	                           String inGroupId, String inArtifactId, String inVersion,
	                           String outGroupId, String outArtifactId, String outVersion,
	                           String pathToJars) throws TransformationFailedException {
		MavenXpp3Reader pomReader = new MavenXpp3Reader();
		try (FileReader reader = new FileReader(inPomFile)) {
			Model model = pomReader.read(reader);
			Dependency target = null;

			for(Dependency dependency :model.getDependencies()) {
				String g = dependency.getGroupId();
				String a = dependency.getArtifactId();
				String v = dependency.getVersion();

				if(g.equals(inGroupId) && a.equals(inArtifactId) && (inVersion == null || v.equals(inVersion))) {
					target = dependency;
					break;
				}
			}

			if(target == null) {
				throw new TransformationFailedException("Dependency " + inGroupId + ":" + inArtifactId + ":" + (inVersion == null ? "*" : inVersion) + " not found in targeted pom.");
			}

			target.setGroupId(outGroupId);
			target.setArtifactId(outArtifactId);
			target.setVersion(outVersion);
			target.setSystemPath(pathToJars + "/" + outArtifactId + "-" + outVersion + "-jar-with-dependencies.jar");
			target.setScope("system");


			MavenXpp3Writer writer = new MavenXpp3Writer();
			writer.write(new FileOutputStream(outPomFile), model);

		} catch (FileNotFoundException e) {
			throw new TransformationFailedException("FileNotFoundException: " + e.getMessage());
		} catch (IOException e) {
			throw new TransformationFailedException("IOException: " + e.getMessage());
		} catch (XmlPullParserException e) {
			throw new TransformationFailedException("XmlPullParserException: " + e.getMessage());
		}
	}
}
