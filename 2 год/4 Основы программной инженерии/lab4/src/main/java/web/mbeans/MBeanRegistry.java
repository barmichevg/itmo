package web.mbeans;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import java.lang.management.ManagementFactory;

public final class MBeanRegistry {
    private static final String DOMAIN = "web.lab4";

    private MBeanRegistry() {
    }

    public static ObjectName register(Object bean, String name) {
        try {
            MBeanServer server = ManagementFactory.getPlatformMBeanServer();
            ObjectName objectName = new ObjectName(DOMAIN + ":type=" + bean.getClass().getSimpleName() + ",name=" + name);

            if (server.isRegistered(objectName)) {
                server.unregisterMBean(objectName);
            }

            server.registerMBean(bean, objectName);
            return objectName;
        } catch (Exception e) {
            throw new IllegalStateException("Cannot register MBean " + name, e);
        }
    }

    public static void unregister(ObjectName objectName) {
        if (objectName == null) {
            return;
        }

        try {
            MBeanServer server = ManagementFactory.getPlatformMBeanServer();
            if (server.isRegistered(objectName)) {
                server.unregisterMBean(objectName);
            }
        } catch (Exception ignored) {
        }
    }
}
