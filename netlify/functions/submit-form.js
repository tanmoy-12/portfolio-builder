exports.handler = async function(event, context) {
    const data = JSON.parse(event.body);
  
    // Process form data and generate portfolio here
  
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Form submission successful' }),
    };
  };
  