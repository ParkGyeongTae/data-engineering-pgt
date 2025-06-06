/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.zeppelin.interpreter.launcher;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.awaitility.Awaitility.await;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.apache.zeppelin.interpreter.remote.RemoteInterpreterManagedProcess;
import org.junit.jupiter.api.Test;

import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.PodStatus;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.server.mock.EnableKubernetesMockClient;

@EnableKubernetesMockClient(https = false, crud = true)
class K8sRemoteInterpreterProcessTest {

  KubernetesClient client;

  @Test
  void testPredefinedPortNumbers() {
    // given
    Properties properties = new Properties();
    Map<String, String> envs = new HashMap<>();

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
        client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "sh",
        "shell",
        properties,
        envs,
        "zeppelin.server.hostname",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        false,
        false);


    // following values are hardcoded in k8s/interpreter/100-interpreter.yaml.
    // when change those values, update the yaml file as well.
    assertEquals("12321:12321", intp.getInterpreterPortRange());
    assertEquals(22321, intp.getSparkDriverPort());
    assertEquals(22322, intp.getSparkBlockManagerPort());
    intp.close();
  }

  @Test
  void testGetTemplateBindings() {
    // given
    Properties properties = new Properties();
    properties.put("my.key1", "v1");
    Map<String, String> envs = new HashMap<>();
    envs.put("MY_ENV1", "V1");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
        client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "sh",
        "shell",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        false,
        false);

    // when
    Properties p = intp.getTemplateBindings(null);

    // then
    assertEquals("default", p.get("zeppelin.k8s.interpreter.namespace"));
    assertEquals(intp.getPodName(), p.get("zeppelin.k8s.interpreter.pod.name"));
    assertEquals("sh", p.get("zeppelin.k8s.interpreter.container.name"));
    assertEquals("interpreter-container:1.0", p.get("zeppelin.k8s.interpreter.container.image"));
    assertEquals("shared_process", p.get("zeppelin.k8s.interpreter.group.id"));
    assertEquals("sh", p.get("zeppelin.k8s.interpreter.group.name"));
    assertEquals("shell", p.get("zeppelin.k8s.interpreter.setting.name"));
    assertTrue(p.containsKey("zeppelin.k8s.interpreter.localRepo"));
    assertEquals("12321:12321" , p.get("zeppelin.k8s.interpreter.rpc.portRange"));
    assertEquals("zeppelin.server.service" , p.get("zeppelin.k8s.server.rpc.service"));
    assertEquals(12320 , p.get("zeppelin.k8s.server.rpc.portRange"));
    assertEquals("null", p.get("zeppelin.k8s.interpreter.user"));
    assertEquals("v1", p.get("my.key1"));
    assertEquals("V1", envs.get("MY_ENV1"));

    envs = (HashMap<String, String>) p.get("zeppelin.k8s.envs");
    assertTrue(envs.containsKey("SERVICE_DOMAIN"));
    assertTrue(envs.containsKey("ZEPPELIN_HOME"));
    intp.close();
  }

  @Test
  void testGetTemplateBindingsForSpark() {
    // given
    Properties properties = new Properties();
    properties.put("my.key1", "v1");
    properties.put("spark.master", "k8s://http://api");
    properties.put("spark.jars.ivy", "my_ivy_path");
    properties.put("spark.driver.extraJavaOptions", "-Dextra_option");
    Map<String, String> envs = new HashMap<>();
    envs.put("MY_ENV1", "V1");
    envs.put("SPARK_SUBMIT_OPTIONS", "my options");
    envs.put("SERVICE_DOMAIN", "mydomain");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        false,
        false);

    // when
    Properties p = intp.getTemplateBindings("mytestUser");

    // then
    assertEquals("spark-container:1.0", p.get("zeppelin.k8s.spark.container.image"));
    assertEquals(String.format("//4040-%s.%s", intp.getPodName(), "mydomain"), p.get("zeppelin.spark.uiWebUrl"));

    envs = (HashMap<String, String>) p.get("zeppelin.k8s.envs");
    assertTrue( envs.containsKey("SPARK_HOME"));
    assertTrue( envs.containsKey("SPARK_DRIVER_EXTRAJAVAOPTIONS_CONF"));
    String driverExtraOptions = envs.get("SPARK_DRIVER_EXTRAJAVAOPTIONS_CONF");
    assertTrue(driverExtraOptions.contains("-Dextra_option"));

    String sparkSubmitOptions = envs.get("SPARK_SUBMIT_OPTIONS");
    assertTrue(sparkSubmitOptions.startsWith("my options"));
    String zeppelinSparkConf = envs.get("ZEPPELIN_SPARK_CONF");
    assertTrue(zeppelinSparkConf.contains("spark.kubernetes.namespace=default"));
    assertTrue(zeppelinSparkConf.contains("spark.kubernetes.driver.pod.name=" + intp.getPodName()));
    assertTrue(zeppelinSparkConf.contains("spark.kubernetes.container.image=spark-container:1.0"));
    assertTrue(zeppelinSparkConf.contains("spark.driver.host=" + intp.getPodName() + ".default.svc"));
    assertTrue(zeppelinSparkConf.contains("spark.driver.port=" + intp.getSparkDriverPort()));
    assertTrue(zeppelinSparkConf.contains("spark.blockManager.port=" + intp.getSparkBlockManagerPort()));
    assertTrue(zeppelinSparkConf.contains("spark.jars.ivy=my_ivy_path"));
    assertFalse(zeppelinSparkConf.contains("--proxy-user"));
    assertTrue(intp.isSpark());
    intp.close();
  }

  @Test
  void testGetTemplateBindingsForSparkWithProxyUser() {
    // given
    Properties properties = new Properties();
    properties.put("my.key1", "v1");
    properties.put("spark.master", "k8s://http://api");
    Map<String, String> envs = new HashMap<>();
    envs.put("MY_ENV1", "V1");
    envs.put("SPARK_SUBMIT_OPTIONS", "my options");
    envs.put("SERVICE_DOMAIN", "mydomain");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        true,
        false);

    // when
    Properties p = intp.getTemplateBindings("mytestUser");
    // then
    assertEquals("spark-container:1.0", p.get("zeppelin.k8s.spark.container.image"));
    assertEquals(String.format("//4040-%s.%s", intp.getPodName(), "mydomain"), p.get("zeppelin.spark.uiWebUrl"));
    assertEquals("mytestUser", p.get("zeppelin.k8s.interpreter.user"));

    envs = (HashMap<String, String>) p.get("zeppelin.k8s.envs");
    assertTrue( envs.containsKey("SPARK_HOME"));

    String sparkSubmitOptions = envs.get("SPARK_SUBMIT_OPTIONS");
    assertTrue(sparkSubmitOptions.startsWith("my options"));
    String zeppelinSparkConf = envs.get("ZEPPELIN_SPARK_CONF");
    assertTrue(zeppelinSparkConf.contains("spark.kubernetes.namespace=default"));
    assertTrue(zeppelinSparkConf.contains("spark.kubernetes.driver.pod.name=" + intp.getPodName()));
    assertTrue(zeppelinSparkConf.contains("spark.kubernetes.container.image=spark-container:1.0"));
    assertTrue(zeppelinSparkConf.contains("spark.driver.host=" + intp.getPodName() + ".default.svc"));
    assertTrue(zeppelinSparkConf.contains("spark.driver.port=" + intp.getSparkDriverPort()));
    assertTrue(zeppelinSparkConf.contains("spark.blockManager.port=" + intp.getSparkBlockManagerPort()));
    assertTrue(zeppelinSparkConf.contains("--proxy-user|mytestUser"));
    assertTrue(intp.isSpark());
    intp.close();
  }

  @Test
  void testGetTemplateBindingsForSparkWithProxyUserAnonymous() {
    // given
    Properties properties = new Properties();
    properties.put("my.key1", "v1");
    properties.put("spark.master", "k8s://http://api");
    Map<String, String> envs = new HashMap<>();
    envs.put("MY_ENV1", "V1");
    envs.put("SPARK_SUBMIT_OPTIONS", "my options");
    envs.put("SERVICE_DOMAIN", "mydomain");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        true,
        false);

    // when
    Properties p = intp.getTemplateBindings("anonymous");
    // then
    assertEquals("spark-container:1.0", p.get("zeppelin.k8s.spark.container.image"));
    assertEquals(String.format("//4040-%s.%s", intp.getPodName(), "mydomain"), p.get("zeppelin.spark.uiWebUrl"));

    envs = (HashMap<String, String>) p.get("zeppelin.k8s.envs");
    assertTrue( envs.containsKey("SPARK_HOME"));

    String sparkSubmitOptions = envs.get("SPARK_SUBMIT_OPTIONS");
    assertFalse(sparkSubmitOptions.contains("--proxy-user"));
    assertTrue(intp.isSpark());
    intp.close();
  }

  @Test
  void testSparkUiWebUrlTemplate() {
    // given
    Properties properties = new Properties();
    Map<String, String> envs = new HashMap<>();
    envs.put("SERVICE_DOMAIN", "mydomain");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        false,
        false);

    // when non template url
    assertEquals("static.url",
        intp.sparkUiWebUrlFromTemplate(
            "static.url",
            4040,
            "zeppelin-server",
            "my.domain.com"));

    // when template url
    assertEquals("//4040-zeppelin-server.my.domain.com",
        intp.sparkUiWebUrlFromTemplate(
            "//{{PORT}}-{{SERVICE_NAME}}.{{SERVICE_DOMAIN}}",
            4040,
            "zeppelin-server",
            "my.domain.com"));
    intp.close();
  }

  @Test
  void testSparkPodResources() {
    // given
    Properties properties = new Properties();
    properties.put("spark.driver.memory", "1g");
    properties.put("spark.driver.cores", "1");
    Map<String, String> envs = new HashMap<>();
    envs.put("SERVICE_DOMAIN", "mydomain");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        false,
        false);

    // when
    Properties p = intp.getTemplateBindings(null);

    // then
    assertEquals("1", p.get("zeppelin.k8s.interpreter.cores"));
    assertEquals("1408Mi", p.get("zeppelin.k8s.interpreter.memory"));
    intp.close();
  }

  @Test
  void testSparkPodResourcesMemoryOverhead() {
    // given
    Properties properties = new Properties();
    properties.put("spark.driver.memory", "1g");
    properties.put("spark.driver.memoryOverhead", "256m");
    properties.put("spark.driver.cores", "5");
    Map<String, String> envs = new HashMap<>();
    envs.put("SERVICE_DOMAIN", "mydomain");

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
        client,
        "default",
        new File(".skip"),
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10,
        10,
        false,
        false);

    // when
    Properties p = intp.getTemplateBindings(null);

    // then
    assertEquals("5", p.get("zeppelin.k8s.interpreter.cores"));
    assertEquals("1280Mi", p.get("zeppelin.k8s.interpreter.memory"));
  }

  @Test
  void testK8sStartSuccessful() throws IOException {
    // given
    Properties properties = new Properties();
    Map<String, String> envs = new HashMap<>();
    envs.put("SERVICE_DOMAIN", "mydomain");
    URL url = Thread.currentThread().getContextClassLoader()
        .getResource("k8s-specs/interpreter-spec.yaml");
    File file = new File(url.getPath());

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        file,
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        10000,
        10,
        false,
        true);
    ExecutorService service = Executors.newFixedThreadPool(1);
    service
      .submit(new PodStatusSimulator(client, intp.getInterpreterNamespace(), intp.getPodName(), intp));
    intp.start("TestUser");
    // then
    assertEquals("Running", intp.getPodPhase());
  }

  @Test
  void testK8sStartFailed() {
    // given
    Properties properties = new Properties();
    Map<String, String> envs = new HashMap<>();
    envs.put("SERVICE_DOMAIN", "mydomain");
    URL url = Thread.currentThread().getContextClassLoader()
        .getResource("k8s-specs/interpreter-spec.yaml");
    File file = new File(url.getPath());

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        file,
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        3000,
        10,
        false,
        true);
    PodStatusSimulator podStatusSimulator = new PodStatusSimulator(client, intp.getInterpreterNamespace(), intp.getPodName(), intp);
    podStatusSimulator.setSecondPhase("Failed");
    podStatusSimulator.setSuccessfulStart(false);
    ExecutorService service = Executors.newFixedThreadPool(1);
    service
        .submit(podStatusSimulator);
    // should throw an IOException
    IOException e = assertThrows(IOException.class, () -> {
      intp.start("TestUser");
    });
    assertNotNull(e);
    // Check that the Pod is deleted
    assertNull(
        client.pods().inNamespace(intp.getInterpreterNamespace()).withName(intp.getPodName())
              .get());
  }

  @Test
  void testK8sStartTimeoutPending() throws InterruptedException {
    // given
    Properties properties = new Properties();
    Map<String, String> envs = new HashMap<>();
    envs.put("SERVICE_DOMAIN", "mydomain");
    URL url = Thread.currentThread().getContextClassLoader()
        .getResource("k8s-specs/interpreter-spec.yaml");
    File file = new File(url.getPath());

    K8sRemoteInterpreterProcess intp = new K8sRemoteInterpreterProcess(
      client,
        "default",
        file,
        "interpreter-container:1.0",
        "shared_process",
        "spark",
        "myspark",
        properties,
        envs,
        "zeppelin.server.service",
        12320,
        false,
        "spark-container:1.0",
        3000,
        10,
        false,
        false);
    PodStatusSimulator podStatusSimulator = new PodStatusSimulator(client, intp.getInterpreterNamespace(), intp.getPodName(), intp);
    podStatusSimulator.setFirstPhase("Pending");
    podStatusSimulator.setSecondPhase("Pending");
    podStatusSimulator.setSuccessfulStart(false);
    ExecutorService service = Executors.newFixedThreadPool(2);
    service
        .submit(podStatusSimulator);
    service.submit(() -> {
      try {
        intp.start("TestUser");
      } catch (IOException e) {
      }
    });
    // wait a little bit
    TimeUnit.SECONDS.sleep(5);
    service.shutdownNow();
    // wait for a shutdown
    service.awaitTermination(10, TimeUnit.SECONDS);
    // Check that the Pod is deleted
    assertNull(client.pods().inNamespace(intp.getInterpreterNamespace())
        .withName(intp.getPodName()).get());

  }

  class PodStatusSimulator implements Runnable {

    private final KubernetesClient client;
    private final String namespace;
    private final String podName;
    private final RemoteInterpreterManagedProcess process;

    private String firstPhase = "Pending";
    private String secondPhase = "Running";
    private boolean successfulStart = true;

    public PodStatusSimulator(
        KubernetesClient client,
        String namespace,
        String podName,
        RemoteInterpreterManagedProcess process) {
      this.client = client;
      this.namespace = namespace;
      this.podName = podName;
      this.process = process;
    }

    public void setFirstPhase(String phase) {
      this.firstPhase = phase;
    }
    public void setSecondPhase(String phase) {
      this.secondPhase = phase;
    }
    public void setSuccessfulStart(boolean successful) {
      this.successfulStart = successful;
    }

    @Override
    public void run() {
      await().until(() -> client.pods().inNamespace(namespace).withName(podName).get() != null);
      // Pod is present set first phase
      Pod pod = client.pods().inNamespace(namespace).withName(podName).get();
      pod.setStatus(new PodStatus());
      pod.getStatus().setPhase(firstPhase);
      client.pods().inNamespace(namespace).resource(pod).update();
      await().pollDelay(Duration.ofMillis(200)).until(() -> firstPhase.equals(
          client.pods().inNamespace(namespace).withName(podName).get().getStatus().getPhase()));
      // Set second Phase
      pod = client.pods().inNamespace(namespace).withName(podName).get();
      pod.getStatus().setPhase(secondPhase);
      client.pods().inNamespace(namespace).resource(pod).update();
      await().pollDelay(Duration.ofMillis(200)).until(() -> secondPhase.equals(
          client.pods().inNamespace(namespace).withName(podName).get().getStatus().getPhase()));
      if (successfulStart) {
        process.processStarted(12320, "testing");
      }
    }
  }

}
