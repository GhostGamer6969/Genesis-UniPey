# UniPey <!-- omit in toc -->

> The app that lets you pay, _basically_, ANYONE, ANYWHERE, and in ANY CURRENCY.



## Table of Contents <!-- omit in toc -->

-   [Development Instructions](#development-instructions)
-   [Where to Start in this Repository?](#where-to-start-in-this-repository)
    -   [NeoX T4](#neox-t4)
        -   [Basic HTML and CSS Structure](#basic-html-and-css-structure)
        -   [NeoX T4 Integrations](#neox-t4-integrations)
-   [Code Explanations](#code-explanations)
    -   [HTML Structure](#html-structure)
    -   [CSS Styling](#css-styling)
    -   [JavaScript Functions](#javascript-functions)

## Development Instructions

To get started with UniPey, follow these steps:

1. **Clone the repository:**

    Clone the code repository to your local machine using the following command:

    ```bash
    git clone https://github.com/GhostGamer6969/Genesis-UniPey.git
    ```

2. **Navigate to the project directory:**

    Change into the repository's directory:

    ```bash
    cd Genesis-UniPey
    ```

3. **Open the application:**

    Open the `index.html` file in your preferred web browser to view the local development site. This file serves as the main entry point for the UniPey application.

## Where to Start in this Repository?

We've documented everything thoroughly in this repository, so feel free to explore wherever you like. However, we recommend starting with the following areas:

### NeoX T4

The heart of UniPey is its integration with the NeoX T4 blockchain. This integration handles everything from connecting to the network to creating and submitting transactions.

#### Basic HTML and CSS Structure

The front-end of the application is built using basic HTML and CSS, making it easy to understand and modify. The main structure of the application can be found in the `index.html` file, with styles located in the `styles.css` file.

- **`index.html`**: This file contains the core structure of the web page, including the header, main content, and footer.
- **`styles.css`**: This file defines the appearance of the application, ensuring a cohesive and responsive design with styles for layout, typography, colors, and interactive elements.

#### NeoX T4 Integrations

All interactions with the NeoX T4 blockchain are handled in the `neox.js` file located in the `/src/lib/neox/` directory. This includes functions for connecting to the blockchain, creating transactions, and querying data.

- **`/src/lib/neox/neoxQueries.js`**: Contains functions for querying information from the NeoX T4 network, such as retrieving account balances and transaction histories.
- **`/src/lib/neox/neoxTransactions.js`**: Contains functions for creating and submitting various types of transactions on the NeoX T4 blockchain, such as transferring tokens or interacting with smart contracts.

## Code Explanations

### HTML Structure

The `index.html` file contains the basic structure of the web application. It is organized using semantic HTML elements to create a clear and accessible layout.

- **Header**: Contains the navigation menu and logo of the application.
- **Main Content**: This section displays the primary user interface elements, such as forms for creating transactions or viewing account information.
- **Footer**: Includes additional links and information about the application.

### CSS Styling

The `styles.css` file defines the appearance of the web application. It includes styles for:

- **Global Styles**: Sets default font sizes, colors, and box model properties to maintain consistency throughout the application.
- **Layout**: Defines the overall structure, including the positioning of the header, main content, and footer.
- **Buttons and Forms**: Styles for interactive elements such as buttons and input fields, ensuring they are visually appealing and consistent.

### JavaScript Functions

The `neox.js` file contains all the necessary JavaScript functions to interact with the NeoX T4 blockchain. This file is essential for handling blockchain operations and includes:

- **Connecting to the NeoX T4 Network**: Establishes a connection to the NeoX T4 blockchain, allowing the app to send and receive data.
- **Creating Transactions**: Functions that build and sign transactions, such as transferring tokens or creating new accounts.
- **Querying Data**: Functions to query the blockchain for data, such as retrieving an account's balance or transaction history.

Each function is documented with comments, explaining its purpose and how to use it. These functions are triggered from the `index.html` file using event listeners attached to buttons and form submissions.

This structure ensures a clear separation of concerns, with HTML handling the structure, CSS handling the appearance, and JavaScript handling the behavior and blockchain interactions. Feel free to modify and extend the code as needed.
