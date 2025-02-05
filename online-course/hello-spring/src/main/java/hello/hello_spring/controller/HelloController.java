package hello.hello_spring.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class HelloController {

    private final Logger logger = LoggerFactory.getLogger(getClass());

    @GetMapping("hello")
    public String hello(Model model) {
        String methodName = new Object() {}.getClass().getEnclosingMethod().getName();

        logger.info("[{}] Start: Handling GET request for /hello", methodName);
        double startTime = System.currentTimeMillis();

        model.addAttribute("data", "spring!!!!");

        logger.info("[{}] End: Returning 'hello' view", methodName);
        double endTime = System.currentTimeMillis();
        logger.info("[{}] Execution Time: {} ms", methodName, (endTime - startTime));

        return "hello";
    }

    @GetMapping("hello-mvc")
    public String helloMvc(@RequestParam("name") String name, Model model) {
        model.addAttribute("name", name);
        return "hello-template";
    }

    @GetMapping("hello-string")
    @ResponseBody
    public String helloString(@RequestParam("name") String name) {
        return "hello" + name;
    }

    @GetMapping("hello-api")
    @ResponseBody
    public Hello helloApi(@RequestParam("name") String name) {
        Hello hello = new Hello();
        hello.setName(name);
        return hello;
    }

    static class Hello {
        private String name;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }
}
