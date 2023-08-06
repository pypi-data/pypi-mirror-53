import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from "@jupyterlab/application";

import { each } from "@phosphor/algorithm";
import { IFileBrowserFactory } from "@jupyterlab/filebrowser";
import { ServerConnection } from "@jupyterlab/services";
import { URLExt, ISettingRegistry } from "@jupyterlab/coreutils";
import { showErrorMessage } from "@jupyterlab/apputils";

const DIRECTORIES_URL = "directories";
const EXTRACT_ARCHVE_URL = "extract-archive";

namespace CommandIDs {
  export const download_archive = "filebrowser:download-archive";
  export const extract_archive = "filebrowser:extract-archive";
}

function downloadArchiveRequest(
  path: string,
  archiveFormat: string
): Promise<void> {
  const settings = ServerConnection.makeSettings();

  let baseUrl = settings.baseUrl;
  let url = URLExt.join(baseUrl, DIRECTORIES_URL, URLExt.encodeParts(path));

  const fullurl = new URL(url);

  // Generate a random token.
  const rand = () =>
    Math.random()
      .toString(36)
      .substr(2);
  const token = (length: number) =>
    (rand() + rand() + rand() + rand()).substr(0, length);

  fullurl.searchParams.append("archiveToken", token(20));
  fullurl.searchParams.append("archiveFormat", archiveFormat);

  const xsrfTokenMatch = document.cookie.match("\\b_xsrf=([^;]*)\\b");
  if (xsrfTokenMatch) {
    fullurl.searchParams.append("_xsrf", xsrfTokenMatch[1]);
  }

  url = fullurl.toString();

  // Check the browser is Chrome https://stackoverflow.com/a/9851769
  const chrome = (window as any).chrome;
  const isChrome = !!chrome && (!!chrome.webstore || !!chrome.runtime);
  if (isChrome) {
    // Workaround https://bugs.chromium.org/p/chromium/issues/detail?id=455987
    window.open(url);
  } else {
    let element = document.createElement("a");
    document.body.appendChild(element);
    element.setAttribute('href', url);
    element.setAttribute('download', '');
    element.click();
    document.body.removeChild(element);
  }

  return void 0;
}

function extractArchiveRequest(path: string): Promise<void> {
  const settings = ServerConnection.makeSettings();

  let baseUrl = settings.baseUrl;
  let url = URLExt.join(baseUrl, EXTRACT_ARCHVE_URL, URLExt.encodeParts(path));

  const fullurl = new URL(url);

  const xsrfTokenMatch = document.cookie.match("\\b_xsrf=([^;]*)\\b");
  if (xsrfTokenMatch) {
    fullurl.searchParams.append("_xsrf", xsrfTokenMatch[1]);
  }

  url = fullurl.toString();
  const request = { method: "GET" };

  return ServerConnection.makeRequest(url, request, settings).then(response => {
    if (response.status !== 200) {
      throw new ServerConnection.ResponseError(response);
    }
  });
}

/**
 * Initialization data for the jupyter-archive extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: "@jupyterlab/archive:archive",
  autoStart: true,

  requires: [IFileBrowserFactory, ISettingRegistry],

  activate: (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    settingRegistry: ISettingRegistry
  ) => {
    console.log("JupyterLab extension jupyter-archive is activated!");

    const { commands } = app;
    const { tracker } = factory;

    let archiveFormat: string = "zip";

    // Load the settings
    settingRegistry
      .load("@hadim/jupyter-archive:archive")
      .then(settings => {
        settings.changed.connect(settings => {
          archiveFormat = settings.get("format").composite as string;
        });
        archiveFormat = settings.get("format").composite as string;
      })
      .catch(reason => {
        console.error(reason);
        showErrorMessage(
          "Fail to read settings for '@jupyterlab/archive:archive'",
          reason
        );
      });

    const selectorOnlyDir = '.jp-DirListing-item[data-isdir="true"]';

    // Add the command to the file's menu.
    commands.addCommand(CommandIDs.download_archive, {
      execute: () => {
        const widget = tracker.currentWidget;
        if (widget) {
          each(widget.selectedItems(), item => {
            if (item.type == "directory") {
              downloadArchiveRequest(item.path, archiveFormat);
            }
          });
        }
      },
      iconClass: "jp-MaterialIcon jp-DownloadIcon",
      label: "Download as an archive"
    });

    app.contextMenu.addItem({
      command: CommandIDs.download_archive,
      selector: selectorOnlyDir,
      rank: 10
    });

    // Add the command to the file's menu.
    commands.addCommand(CommandIDs.extract_archive, {
      execute: () => {
        const widget = tracker.currentWidget;
        if (widget) {
          each(widget.selectedItems(), item => {
            extractArchiveRequest(item.path);
          });
        }
      },
      iconClass: "jp-MaterialIcon jp-DownCaretIcon",
      label: "Extract archive"
    });

    // Add a command for each archive extensions
    // TODO: use only one command and accept multiple extensions.
    const allowedArchiveExtensions = [".zip", ".tgz", ".tar.gz",".tbz", ".tbz2",
                                      ".tar.bz", ".tar.bz2", ".txz", ".tar.xz"]

    allowedArchiveExtensions.forEach(extension => {
      const selector = '.jp-DirListing-item[title$="' + extension + '"]';
      app.contextMenu.addItem({
        command: CommandIDs.extract_archive,
        selector: selector,
        rank: 10
      });
    });

  }
};

export default extension;
