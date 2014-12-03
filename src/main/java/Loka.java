import org.slf4j.Logger;
import org.spongepowered.api.event.state.PreInitializationEvent;
import org.spongepowered.api.event.state.ServerStoppingEvent;
import org.spongepowered.api.plugin.Plugin;
import org.spongepowered.api.util.event.Subscribe;

@Plugin(id = "Loka", name = "Loka", version = "4.0")
public class Loka {
    private Logger log;

    @Subscribe
    public void onInit(PreInitializationEvent event) {
        // TODO -> start plugin: load config, assign variables
        log = event.getPluginLog();
        log.info("Plugin enabled.");
    }

    @Subscribe
    public void onStop(ServerStoppingEvent event) {
        // TODO -> stop plugin: save config (if changed), clean up
        log.info("Plugin disabled.");
    }
}
