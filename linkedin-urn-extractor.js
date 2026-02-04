/**
 * LinkedIn Profile URN Extractor
 *
 * PURPOSE:
 * Extracts a LinkedIn profile URN from a given vanityName (profile ID) without
 * requiring a browser or JavaScript execution. Uses simple HTTP requests.
 *
 * HOW IT WORKS:
 * 1. Makes an HTTP GET request to the LinkedIn profile page
 * 2. Parses the HTML response for <code> tags containing profile data
 * 3. Identifies the target profile URN by finding it near the publicIdentifier field
 * 4. Distinguishes between viewer URN (logged-in user) and target profile URN
 *
 * REQUIREMENTS:
 * - Valid li_at and JSESSIONID cookies from an authenticated LinkedIn session
 * - User-Agent string from your browser
 * - node-fetch package (npm install node-fetch)
 *
 * AUTHENTICATION:
 * The script requires cookies from an active LinkedIn session. These can be obtained from:
 * - Browser DevTools → Application → Cookies → linkedin.com
 * - Look for: li_at and JSESSIONID cookies
 *
 * @author LinkedIn URN Extraction Tool
 * @version 1.0.0
 */

import { readFileSync } from 'fs';
import fetch from 'node-fetch';

/**
 * Configuration structure
 * @typedef {Object} LinkedInConfig
 * @property {Object} cookies - Authentication cookies
 * @property {string} cookies.li_at - LinkedIn authentication token
 * @property {string} cookies.JSESSIONID - Session identifier
 * @property {string} userAgent - Browser user-agent string
 */

/**
 * Result structure for URN extraction
 * @typedef {Object} URNExtractionResult
 * @property {boolean} success - Whether extraction succeeded
 * @property {string} vanityName - Input profile ID
 * @property {string} [profileUrn] - Extracted profile URN (if successful)
 * @property {string} [error] - Error message (if failed)
 * @property {string} [method] - Method used for extraction
 */

/**
 * Main class for LinkedIn URN extraction
 */
export class LinkedInURNExtractor {
  /**
   * @param {string} configPath - Path to config.json file
   */
  constructor(configPath = './config.json') {
    this.config = this.loadConfig(configPath);
  }

  /**
   * Load configuration from JSON file
   * @private
   */
  loadConfig(configPath) {
    try {
      return JSON.parse(readFileSync(configPath, 'utf-8'));
    } catch (error) {
      throw new Error(`Failed to load config from ${configPath}: ${error.message}`);
    }
  }

  /**
   * Extract profile URN for a given LinkedIn vanityName
   *
   * @param {string} vanityName - LinkedIn profile ID (e.g., "chrisweavill")
   * @param {boolean} [verbose=false] - Enable detailed logging
   * @returns {Promise<URNExtractionResult>}
   *
   * @example
   * const extractor = new LinkedInURNExtractor();
   * const result = await extractor.getProfileUrn('chrisweavill');
   * if (result.success) {
   *   console.log(result.profileUrn);
   * }
   */
  async getProfileUrn(vanityName, verbose = false) {
    if (verbose) console.log(`🔍 Extracting URN for: ${vanityName}\n`);

    try {
      // Step 1: Fetch profile page HTML
      const html = await this.fetchProfilePage(vanityName, verbose);

      // Step 2: Extract URN using primary method
      let targetUrn = this.extractFromCodeTags(html, vanityName, verbose);

      // Step 3: Fallback to occurrence-based method if needed
      if (!targetUrn) {
        if (verbose) console.log(`⚠️  Primary method failed, using fallback...\n`);
        targetUrn = this.extractByOccurrenceCount(html, verbose);
      }

      if (!targetUrn) {
        return {
          success: false,
          vanityName,
          error: 'No profile URN found in HTML'
        };
      }

      if (verbose) console.log(`✅ Successfully extracted URN: ${targetUrn}\n`);

      return {
        success: true,
        vanityName,
        profileUrn: targetUrn,
        method: 'code_tag_extraction'
      };

    } catch (error) {
      return {
        success: false,
        vanityName,
        error: error.message
      };
    }
  }

  /**
   * Fetch LinkedIn profile page HTML
   * @private
   */
  async fetchProfilePage(vanityName, verbose) {
    const url = `https://www.linkedin.com/in/${vanityName}/`;

    const response = await fetch(url, {
      headers: {
        'cookie': `li_at=${this.config.cookies.li_at}; JSESSIONID=${this.config.cookies.JSESSIONID}`,
        'user-agent': this.config.userAgent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none'
      },
      redirect: 'manual'
    });

    // Handle HTTP errors
    if (response.status === 404) {
      throw new Error('Profile not found (404)');
    }

    if (response.status === 302 || response.status === 301) {
      const location = response.headers.get('location');
      if (location && location.includes('/authwall')) {
        throw new Error('Authentication required - cookies may be expired');
      }
      throw new Error(`Profile redirected to: ${location}`);
    }

    if (response.status !== 200) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const html = await response.text();

    if (verbose) {
      console.log(`✅ Fetched profile page (${html.length} bytes)\n`);
    }

    return html;
  }

  /**
   * Extract target profile URN from <code> tags
   *
   * METHOD:
   * LinkedIn embeds profile data in <code> tags within the HTML.
   * The target profile URN appears near the publicIdentifier field.
   * We find the <code> tag containing the vanityName and extract
   * the URN that appears BEFORE the publicIdentifier field.
   *
   * WHY THIS WORKS:
   * - Target profile URN is defined first in identityDashProfilesByMemberIdentity
   * - Viewer's URN appears later or in different contexts
   * - publicIdentifier field contains the vanityName
   *
   * @private
   */
  extractFromCodeTags(html, vanityName, verbose) {
    if (verbose) {
      console.log(`🔎 Method 1: Extracting from <code> tags...\n`);
    }

    const codeRegex = /<code[^>]*>(.*?)<\/code>/gs;
    let codeMatch;

    while ((codeMatch = codeRegex.exec(html)) !== null) {
      // Decode HTML entities
      const codeContent = codeMatch[1]
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>');

      // Check if this <code> tag contains the vanityName
      if (codeContent.includes(vanityName)) {
        const urnRegex = /urn:li:fsd_profile:[A-Za-z0-9_-]+/g;
        const urnsInCode = [...new Set(codeContent.match(urnRegex) || [])];

        if (urnsInCode.length === 0) continue;

        if (verbose) {
          console.log(`   ✓ Found <code> tag containing "${vanityName}"`);
          console.log(`   URNs in tag: ${urnsInCode.join(', ')}\n`);
        }

        // Find publicIdentifier position
        const publicIdentifierIndex = codeContent.indexOf(`"publicIdentifier":"${vanityName}"`);

        if (publicIdentifierIndex !== -1) {
          // Get URNs appearing BEFORE publicIdentifier
          const urnsBeforePublicId = urnsInCode
            .map(urn => ({
              urn,
              index: codeContent.indexOf(urn)
            }))
            .filter(item => item.index !== -1 && item.index < publicIdentifierIndex)
            .sort((a, b) => a.index - b.index);

          if (urnsBeforePublicId.length > 0) {
            const targetUrn = urnsBeforePublicId[0].urn;
            if (verbose) {
              console.log(`   🎯 Selected URN (appears before publicIdentifier): ${targetUrn}\n`);
            }
            return targetUrn;
          }
        }

        // Fallback: use first URN in the tag
        if (verbose) {
          console.log(`   🎯 Using first URN from tag: ${urnsInCode[0]}\n`);
        }
        return urnsInCode[0];
      }
    }

    return null;
  }

  /**
   * Extract URN based on occurrence count (fallback method)
   *
   * METHOD:
   * The viewer's URN appears more frequently in the HTML (navigation, menus, etc.)
   * The target profile's URN appears less frequently.
   * We count occurrences and select the one with FEWEST occurrences.
   *
   * NOTE: This is less reliable than extractFromCodeTags()
   *
   * @private
   */
  extractByOccurrenceCount(html, verbose) {
    if (verbose) {
      console.log(`🔎 Method 2: Extracting by occurrence count...\n`);
    }

    const urnRegex = /urn:li:fsd_profile:[A-Za-z0-9_-]+/g;
    const allUrns = [...new Set(html.match(urnRegex) || [])];

    if (allUrns.length === 0) {
      return null;
    }

    // Count occurrences
    const urnCounts = {};
    allUrns.forEach(urn => {
      const escapedUrn = urn.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const count = (html.match(new RegExp(escapedUrn, 'g')) || []).length;
      urnCounts[urn] = count;

      if (verbose) {
        console.log(`   ${urn}: ${count} occurrences`);
      }
    });

    // Select URN with fewest occurrences (target profile)
    let targetUrn = allUrns[0];
    let minCount = urnCounts[allUrns[0]];

    for (const urn of allUrns) {
      if (urnCounts[urn] < minCount) {
        minCount = urnCounts[urn];
        targetUrn = urn;
      }
    }

    if (verbose) {
      console.log(`\n   🎯 Selected URN (fewest occurrences): ${targetUrn}\n`);
    }

    return targetUrn;
  }

  /**
   * Extract URNs for multiple profiles (batch processing)
   *
   * @param {string[]} vanityNames - Array of LinkedIn profile IDs
   * @param {number} [delayMs=1000] - Delay between requests (rate limiting)
   * @param {boolean} [verbose=false] - Enable detailed logging
   * @returns {Promise<URNExtractionResult[]>}
   *
   * @example
   * const extractor = new LinkedInURNExtractor();
   * const results = await extractor.getBatch(['chrisweavill', 'satyanadella']);
   */
  async getBatch(vanityNames, delayMs = 1000, verbose = false) {
    const results = [];

    for (let i = 0; i < vanityNames.length; i++) {
      const vanityName = vanityNames[i];
      const result = await this.getProfileUrn(vanityName, verbose);
      results.push(result);

      // Rate limiting: wait between requests
      if (i < vanityNames.length - 1) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    }

    return results;
  }
}

/**
 * CLI Interface
 * Usage: node linkedin-urn-extractor.js <vanityName> [--verbose]
 */
// Check if running as CLI (not imported as module)
const isMainModule = process.argv[1] && process.argv[1].endsWith('linkedin-urn-extractor.js');

if (isMainModule) {
  const args = process.argv.slice(2);
  const verbose = args.includes('--verbose') || args.includes('-v');
  const vanityNames = args.filter(arg => !arg.startsWith('--') && !arg.startsWith('-'));

  if (vanityNames.length === 0) {
    console.log('LinkedIn Profile URN Extractor\n');
    console.log('Usage:');
    console.log('  node linkedin-urn-extractor.js <vanityName> [--verbose]');
    console.log('  node linkedin-urn-extractor.js <name1> <name2> ... [--verbose]\n');
    console.log('Options:');
    console.log('  --verbose, -v    Enable detailed logging\n');
    console.log('Examples:');
    console.log('  node linkedin-urn-extractor.js chrisweavill');
    console.log('  node linkedin-urn-extractor.js chrisweavill satyanadella --verbose\n');
    process.exit(1);
  }

  const extractor = new LinkedInURNExtractor();

  if (vanityNames.length === 1) {
    // Single profile
    extractor.getProfileUrn(vanityNames[0], verbose).then(result => {
      if (!verbose) {
        console.log(`🔍 Looking up URN for: ${result.vanityName}\n`);
      }

      if (result.success) {
        console.log('═══════════════════════════════════════════════════════');
        console.log('   SUCCESS');
        console.log('═══════════════════════════════════════════════════════\n');
        console.log(`Input:  ${result.vanityName}`);
        console.log(`Output: ${result.profileUrn}\n`);
        console.log('JSON:');
        console.log(JSON.stringify({
          vanityName: result.vanityName,
          profileUrn: result.profileUrn
        }, null, 2));
        console.log('');
      } else {
        console.log('═══════════════════════════════════════════════════════');
        console.log('   FAILED');
        console.log('═══════════════════════════════════════════════════════\n');
        console.log(`Profile: ${result.vanityName}`);
        console.log(`Error:   ${result.error}\n`);
        process.exit(1);
      }
    }).catch(error => {
      console.error(`\n❌ Fatal error: ${error.message}`);
      process.exit(1);
    });

  } else {
    // Batch mode
    extractor.getBatch(vanityNames, 1000, verbose).then(results => {
      console.log('\n═══════════════════════════════════════════════════════');
      console.log('   BATCH RESULTS');
      console.log('═══════════════════════════════════════════════════════\n');

      const successful = results.filter(r => r.success);
      const failed = results.filter(r => !r.success);

      console.log(`Total: ${results.length} | Success: ${successful.length} | Failed: ${failed.length}\n`);

      if (successful.length > 0) {
        console.log('✅ Successful:');
        successful.forEach(r => {
          console.log(`   ${r.vanityName} → ${r.profileUrn}`);
        });
        console.log('');
      }

      if (failed.length > 0) {
        console.log('❌ Failed:');
        failed.forEach(r => {
          console.log(`   ${r.vanityName}: ${r.error}`);
        });
        console.log('');
      }

      console.log('JSON:');
      console.log(JSON.stringify(results.map(r => ({
        vanityName: r.vanityName,
        profileUrn: r.profileUrn || null,
        success: r.success
      })), null, 2));
      console.log('');

      if (failed.length > 0) {
        process.exit(1);
      }
    }).catch(error => {
      console.error(`\n❌ Fatal error: ${error.message}`);
      process.exit(1);
    });
  }
}
